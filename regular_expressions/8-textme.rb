#!/usr/bin/env ruby
match = ARGV[0].match(/\[from:(.?)\] \[to:(.?)\] \[flags:(.*?)\]/)
puts "#{match[1]},#{match[2]},#{match[3]}" if match
