import urllib2
import json

class ArachniClient(object):

   with open('./profiles/default.json') as f:
      default_profile = json.load(f)

   def __init__(self, arachni_url = 'http://127.0.0.1:7331'):
      self.arachni_url = arachni_url
      self.options = ArachniClient.default_profile

   def get_http_request(self, api_path):
      return urllib2.urlopen(self.arachni_url + api_path).read()

   def post_api(self, api_path):
      options = json.dumps(self.options)
      request = urllib2.Request(self.arachni_url + api_path, options)
      request.add_header('Content-Type', 'application/json')
      return urllib2.urlopen(request).read()

   def put_request(self, api_path):
      request = urllib2.Request(self.arachni_url + api_path)
      request.get_method = lambda: 'PUT'
      return urllib2.urlopen(request).read()

   def delete_request(self, api_path):
      request = urllib2.Request(self.arachni_url + api_path)
      request.get_method = lambda: 'DELETE'
      return urllib2.urlopen(request).read()
      
   def get_scans(self):
      return json.loads(self.get_http_request('/scans'))

   def get_status(self, scan_id):
      return json.loads(self.get_http_request('/scans/' + scan_id))

   def pause_scan(self, scan_id):
      return self.put_request('/scans/' + scan_id + '/pause')

   def resume_scan(self, scan_id):
      return self.put_request('/scans/' + scan_id + '/resume')

   def get_report(self, scan_id, report_format = None):
      if self.get_status(scan_id)['status'] == 'done':

         if report_format == 'html':
            report_format = 'html.zip'

         if report_format in ['json', 'xml', 'yaml', 'html.zip']:
            return self.get_http_request('/scans/' + scan_id + '/report.' + report_format)
         elif report_format == None:
            return self.get_http_request('/scans/' + scan_id + '/report')
         else:
            print 'your requested format is not available.'

      else:
         print 'your requested scan is in progress.'

   def delete_scan(self, scan_id):
      return self.delete_request('/scans/' + scan_id)

   def start_scan(self):
      if self.options['url']:
         return json.loads(self.post_api('/scans'))
      else:
         print 'Target is not set!'

   def target(self, target_url):
      try:
         urllib2.urlopen(target_url)
         self.options['url'] = target_url
      except urllib2.HTTPError, e:
         print e.code

   def profile(self, profile_path):
      with open(profile_path) as f:
         self.options = json.load(f)

if __name__ == '__main__':
   a = ArachniClient()
   a.profile('./profiles/xss.json')
   a.target('http://127.0.0.1:8080')
   print a.start_scan()
