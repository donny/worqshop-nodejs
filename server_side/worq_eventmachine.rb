#!/usr/bin/ruby

# From: http://www.igvita.com/2008/05/27/ruby-eventmachine-the-speed-demon/

require 'rubygems'
require 'eventmachine'
require 'evma_httpserver'
require 'beanstalk-client'
 
class Handler  < EventMachine::Connection
	include EventMachine::HttpServer
 
	def process_http_request
		resp = EventMachine::DelegatedHttpResponse.new( self )
 
		# Block that fulfills the request.
		operation = proc do

				# 'result' is in JSON already.
				result = @http_post_content

				beanstalk = Beanstalk::Pool.new(['127.0.0.1:9000'])
				beanstalk.put(result)

				resp.status = 200
				resp.content = '{"result": "OK"}'
		end
 
		# Callback block to execute once the request is fulfilled.
		callback = proc do |res|
			resp.send_response
		end
 
		# Let the thread pool (20 Ruby threads) handle requests.
		EM.defer(operation, callback)
	end
end
 
EventMachine::run {
	EventMachine.epoll
	EventMachine::start_server("0.0.0.0", 8000, Handler)
	puts "Listening..."
}
