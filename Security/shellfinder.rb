#!/usr/bin/ruby
# Old script to find php scripts on a given site
# Needs to be rewritten in python
# Matt Erasmus <code@zonbi.org>

require 'net/http'

server = ARGV[0]
startpath = ARGV[1]

###  proxy
proxy = 'x.x.x.x'
proxy_port = 'xx'

if ARGV.length != 2 
    puts "#{$0} www.mybrokeasssite.com [ /pathtoscan ]"
    exit
end  

# removed admin.php config.php test1.php index2.php info.php contact.php
# this really needs to be done a little better, perhaps reference a text file ?
kit_name = ["_htdocs.php", "_zboard.php", "1owrsh.php", "404.php", "5008.php", "669127.php", "a813.php", "aaa.php",
            "Aboutus.php", "Absa-co-za.php", "accsess.php", "administrator.php", "afir.php", "archives.php", "art.php", 
            "artwork.php", "aser.php", "auth.php", "back99.php", "basemant.php", "basements.php", "bashrc.php", "bbp.php", 
            "bbs.php", "bm.php", "Bm.php", "board.php", "c.php", "c100.php", "c6546456.php", "c99.php", "carlos.php", 
            "cart.php", "clients.php", "color_picker.php", "com_myblog.php", "comment.php", "company.php", "conf.php", 
            "coni.php", "cp1.php", "d.php", "data.php", "dat.php", "db.php", "dns.php", 
            "dtype.php", "dull.php", "duser.php", "edu.php", "english_language.php", "error.php", "error_log.php", 
            "f.php", "faq.php", "fat.php", "fatal.php", "fb.php", "filesz.php", "fnb-b4nk.php", "fnb-bank.php", "fnb-co-za.php", 
            "functions.php", "FUNCTIONS.php", "global.php", "goodfriend.php", "haru.php", "header.php", "hip.php", 
            "hyrjar.php", "icq.php", "il-language.php", "image.php", "images.php", "img.php", "in.php", "in1.php", "inc.php", 
            "include.php", "index22.php", "index3.php", "indpass.php", "inf.php",  
            "info-secure.php", "ini1.php", "join_us.php", "joomlaxml.php", "k3k3.php", "kdhgalilee.php", "ketek.php", 
            "language.php", "llhdjjxkl.php", "lists.php", "js.php", "log.php", "logo.php", "los.php", "main.php", "ma-hacker.php", 
            "mambo.php", "mem.php", "mm.php", "mod_archiv.php", "mod_stat.php", "mod_class.php", "mode.php", "modes.php", 
            "mtview.php", "n0va.php", "nav.php", "new.php", "newabc.php", "news.php", "neye.php", "nnv.php", "None.php", 
            "offfline.php", "offflines.php", "offline.php", "offlines.php", "perfect.php", "pic.php", "picture_library.php", 
            "pin.php", "popup.php", "pp.php", "print_out.php", "robots.php", "s.php", "sarah.php", "sars.php", "SARS.php", 
            "SARS.php", "sarsss.php", "sas.php", "secured.php", "segzydinho.php", "services.php", "setting.php", "sfv.php", 
            "shell.php", "simple.php", "skin.php", "SnIpEr2.php", "source.php", "spider.php", "src.php", "Statistics.php", 
            "sunnyboy.php", "table.php", "tboy.php", "test.php", "test1.php", "testimonial.php", "testing.php", "tmp.php"    , 
            "tol.php", "toolbar.php", "topdata.php", "tt.php", "uner.php", "update.php", "ups.php", "urlcounts.php", "user.php", 
            "users.php", "uu.php", "vault.php", "view.php", "view_data.php", "views.php", "w.php", "www.php", "y10.php", 
            "ya.php", "yho.php", "yo.php", "zavir.php", "zavir2.php", "zaz.php", "zine.php", "zz.php"]

puts 
puts "[*] PHP Shell finder"
puts
puts "Going to check http://#{server} at #{startpath}"
puts
kit_name.each { |brute|
     http = Net::HTTP::Proxy(proxy, proxy_port).new(server)
     find_lg = startpath + brute 
     headers, body = http.get(find_lg)
     
     puts "CHECKING > #{find_lg}"

     if headers.code =~ /200/
        puts
        print "SHELL FOUND>> http://#{server}#{find_lg}\n"
        puts
        exit
     end 
}

print "Either I'm done and didn't find anything or z0nbi is leeter than he lets on...\n"
