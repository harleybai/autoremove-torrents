Auto Remove Torrents
======================
By modifying project: https://github.com/jerrymakesjelly/autoremove-torrents

####Requirements
* Python 3

That's all. It's a simple but smart program.

####Quick Start
#####Download

    git clone https://github.com/harleybai/autoremove-torrents.git
    cd autoremove-torrents

#####Write your configuration file

In order to satisfactory your needs, you have to learn how to write a configuration file. 

more config to visit [config.yml](https://github.com/harleybai/autoremove-torrents/blob/master/config.yml)

Example:

    my_task:
      client: qbittorrent
      host: http://127.0.0.1
      username: admin
      password: adminadmin
      strategies:
        my_strategy:
          categories:
            - IPT
          seeding_time: 1209600
          ratio: 1
      delete_data: true


      
#####RUN
    autoremove-torrents [-v] [-c=configfilepath] [-t=taskname]
    -v : not delete torrent or data, for viewing result
    -c : the path of config.yml, default for current directory
    -t : taskname, one config.yml can contain many task config, you can choose one task to run

