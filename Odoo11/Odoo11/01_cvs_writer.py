diff -ru odoo.orig/api.py odoo/api.py
--- odoo.orig/api.py	2019-03-11 17:21:50.689527113 +0000
+++ odoo/api.py	2019-03-11 18:09:08.041326395 +0000
@@ -57,6 +57,9 @@
 
 from odoo.tools import frozendict, classproperty
 
+from odoo.tools import config
+import odoo.cvs_writer as cw
+
 _logger = logging.getLogger(__name__)
 
 # The following attributes are used, and reflected on wrapping methods:
@@ -669,6 +672,12 @@
         return obj.env.uid
     return -1
 
+def cvs_write(method_name):
+    cvsw = cw.CvsWriter(config.misc['cvs']['location'])
+
+cvs_write.dispatch = {}
+#cvs_write.dispatch['']
+
 def call_kw_model(method, self, args, kwargs):
     context, args, kwargs = split_context(method, args, kwargs)
     recs = self.with_context(context or {})
diff -ru odoo.orig/tools/config.py odoo/tools/config.py
--- odoo.orig/tools/config.py	2019-03-11 17:21:50.659526629 +0000
+++ odoo/tools/config.py	2019-03-11 17:29:00.286500392 +0000
@@ -12,6 +12,7 @@
 import sys
 import odoo
 from .. import release, conf, loglevels
+from .. import cvs_writer as cw
 from . import appdirs, pycompat
 
 from passlib.context import CryptContext
@@ -550,6 +551,14 @@
             pass
         except ConfigParser.NoSectionError:
             pass
+        cw.CvsWriter(self.misc['cvs']['location'], (
+            'timestamp',
+            'actionName',
+            'actionId',
+            'userId',
+            'ipAddr',
+            'stageId',
+        ))
 
     def save(self):
         p = ConfigParser.RawConfigParser()
