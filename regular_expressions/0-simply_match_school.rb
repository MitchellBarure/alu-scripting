#!/usr/bin/env ruby

text = ARGV[0] || "" 
matches = text.scan(/School/)
puts matches.join 
