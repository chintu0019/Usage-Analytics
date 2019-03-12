diff -x '*.pyc' -x '*.cvs' -Nru odoo.orig/api.py odoo/api.py
--- odoo.orig/api.py	2019-03-11 17:21:50.689527113 +0000
+++ odoo/api.py	2019-03-12 11:59:40.308461147 +0000
@@ -57,6 +57,9 @@
 
 from odoo.tools import frozendict, classproperty
 
+from odoo.tools import config
+import odoo.cvs_writer as cw
+
 _logger = logging.getLogger(__name__)
 
 # The following attributes are used, and reflected on wrapping methods:
@@ -669,21 +672,57 @@
         return obj.env.uid
     return -1
 
+def cvs_write(dispatch, user_id, method_name, recs, params, ids = None):
+    cvsw = cw.CvsWriter(config.misc['cvs']['location'])
+    writer = dispatch.get(method_name, None)
+    if writer != None:
+        writer(cvsw, user_id, method_name, recs, params, ids)
+
+# (no ids)
+cvs_write.model_dis = {}
+cvs_write.model_recs_dis = {}
+
+cvs_write.multi_dis = {}
+cvs_write.multi_recs_dis = {}
+
+
+def create(cvsw, user_id, method_name, recs, params, _):
+    recs_name = str(recs).split('(', 1)[0]
+    writer = cvs_write.model_recs_dis.get(recs_name, None)
+    if writer != None:
+        writer(cvsw, user_id, method_name, recs, params)
+cvs_write.model_dis['create'] = create
+
+
+def create_note(cvsw, user_id, method_name, recs, params):
+    cvsw.write({
+        'actionName': 'Create Note',
+        'userId': user_id,
+        'id': params.args[0]['tag_ids'][0][0],
+        'text': params.args[0]['memo'],
+    })
+cvs_write.model_recs_dis['note.note'] = create_note
+
+
 def call_kw_model(method, self, args, kwargs):
     context, args, kwargs = split_context(method, args, kwargs)
     recs = self.with_context(context or {})
-    _logger.debug("User %s calls %s.%s(%s)", get_user_id(self), recs, method.__name__, Params(args, kwargs))
+    _logger.debug("(Model) ++ User: %s, call method: %s, recs: %s, params: %s", get_user_id(self), method.__name__, recs, Params(args, kwargs))
+    cvs_write(cvs_write.model_dis, get_user_id(self), method.__name__, recs, Params(args, kwargs))
     result = method(recs, *args, **kwargs)
     return downgrade(method, result, recs, args, kwargs)
 
+
 def call_kw_multi(method, self, args, kwargs):
     ids, args = args[0], args[1:]
     context, args, kwargs = split_context(method, args, kwargs)
     recs = self.with_context(context or {}).browse(ids)
-    _logger.debug("User %s calls %s.%s(%s)", get_user_id(self), recs, method.__name__, Params(args, kwargs))
+    _logger.debug("(Multi) ++ User: %s, call method: %s, recs: %s, ids: %s, params: %s", get_user_id(self), method.__name__, recs, ids, Params(args, kwargs))
+    cvs_write(cvs_write.multi_dis, get_user_id(self), method.__name__, recs, Params(args, kwargs), ids)
     result = method(recs, *args, **kwargs)
     return downgrade(method, result, recs, args, kwargs)
 
+
 def call_kw(model, name, args, kwargs):
     """ Invoke the given method ``name`` on the recordset ``model``. """
     method = getattr(type(model), name)
diff -x '*.pyc' -x '*.cvs' -Nru odoo.orig/cvs_writer.py odoo/cvs_writer.py
--- odoo.orig/cvs_writer.py	2019-03-11 17:21:50.699527275 +0000
+++ odoo/cvs_writer.py	2019-03-12 11:59:40.305127764 +0000
@@ -1,42 +1,53 @@
-#!/usr/bin/env python3
-
-import os
-import threading
-import csv
-
-class CvsWriter:
-    writers = {}
-
-    def __init__(self, filename, column_names_tuple = None):
-        if column_names_tuple == None:
-            self._recover(filename)
-        else:
-            self._first_init(filename, column_names_tuple)
-
-    def _recover(self, filename):
-        self.__dict__ = CvsWriter.writers[filename]
-
-    def _first_init(self, filename, column_names_tuple):
-        CvsWriter.writers[filename] = CvsWriter.writers.get(filename, {})
-        self.__dict__ = CvsWriter.writers[filename]
-
-        self.write_lock = threading.Lock()
-        self.column_names = {}
-        self.filename = os.path.abspath(filename)
-
-        label_row = []
-        for idx, column_name in enumerate(column_names_tuple):
-            self.column_names[column_name] = idx
-            label_row.append(column_name)
-
-        with self.write_lock, open(self.filename, 'w') as f:
-            csv.writer(f).writerow(label_row)
-
-    def write(self, elements_dict):
-        with self.write_lock, open(self.filename, 'a') as f:
-            row = ['']*len(self.column_names)
-
-            for column_name, value in elements_dict.items():
-                row[ self.column_names[column_name] ] = str(value)
-
-            csv.writer(f).writerow(row)
\ No newline at end of file
+#!/usr/bin/env python3
+
+import csv
+from datetime import datetime
+import os
+import threading
+
+class CvsWriter:
+    writers = {}
+
+    def __init__(self, filename, column_names_tuple = None):
+        if column_names_tuple == None:
+            self._recover(filename)
+        else:
+            self._first_init(filename, column_names_tuple)
+
+    def _recover(self, filename):
+        self.__dict__ = CvsWriter.writers[filename]
+
+    def _first_init(self, filename, column_names_tuple):
+        CvsWriter.writers[filename] = CvsWriter.writers.get(filename, {})
+        self.__dict__ = CvsWriter.writers[filename]
+
+        self.write_lock = threading.Lock()
+        self.column_names = {}
+        self.filename = os.path.abspath(filename)
+        self.id_to_ip = {}
+
+        label_row = []
+        for idx, column_name in enumerate(column_names_tuple):
+            self.column_names[column_name] = idx
+            label_row.append(column_name)
+
+        with self.write_lock, open(self.filename, 'w') as f:
+            csv.writer(f).writerow(label_row)
+
+    def connect_id_to_ip(self, userId, userIp):
+        with self.write_lock:
+            self.id_to_ip[userId] = userIp
+
+    def write(self, elements_dict):
+        with self.write_lock, open(self.filename, 'a') as f:
+            if 'userId' in elements_dict and not 'ipAddr' in elements_dict:
+                elements_dict['ipAddr'] = self.id_to_ip.get(elements_dict['userId'], '')
+            if not 'timestamp' in elements_dict:
+                elements_dict['timestamp'] = datetime.now()
+
+            row = ['']*len(self.column_names)
+
+            for column_name, value in elements_dict.items():
+                row[ self.column_names[column_name] ] = str(value)
+
+            csv.writer(f).writerow(row)
diff -x '*.pyc' -x '*.cvs' -Nru odoo.orig/http.py odoo/http.py
--- odoo.orig/http.py	2019-03-11 17:21:50.746194695 +0000
+++ odoo/http.py	2019-03-12 11:59:40.308461147 +0000
@@ -51,6 +51,9 @@
 
 from .modules.module import module_manifest
 
+from odoo.tools import config
+import odoo.cvs_writer as cw
+
 _logger = logging.getLogger(__name__)
 rpc_request = logging.getLogger(__name__ + '.rpc.request')
 rpc_response = logging.getLogger(__name__ + '.rpc.response')
@@ -311,6 +314,9 @@
 
     def _call_function(self, *args, **kwargs):
         _logger.debug("User: %s Remote addr: %s", self.uid, self.httprequest.remote_addr)
+        cvsw = cw.CvsWriter (config.misc['cvs']['location'])
+        cvsw.connect_id_to_ip(self.uid, self.httprequest.remote_addr)
+
         request = self
         if self.endpoint.routing['type'] != self._request_type:
             msg = "%s, %s: Function declared as capable of handling request of type '%s' but called with a request of type '%s'"
diff -x '*.pyc' -x '*.cvs' -Nru odoo.orig/tools/config.py odoo/tools/config.py
--- odoo.orig/tools/config.py	2019-03-11 17:21:50.659526629 +0000
+++ odoo/tools/config.py	2019-03-12 11:59:40.308461147 +0000
@@ -12,6 +12,7 @@
 import sys
 import odoo
 from .. import release, conf, loglevels
+from .. import cvs_writer as cw
 from . import appdirs, pycompat
 
 from passlib.context import CryptContext
@@ -550,6 +551,15 @@
             pass
         except ConfigParser.NoSectionError:
             pass
+        cw.CvsWriter(self.misc['cvs']['location'], (
+            'timestamp',
+            'actionName',
+            'userId',
+            'ipAddr',
+            'stageId',
+            'id',
+            'text',
+        ))
 
     def save(self):
         p = ConfigParser.RawConfigParser()