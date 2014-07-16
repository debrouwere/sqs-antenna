profile = 'profile ' + 'newslynx'
queue_name = 'sandbox'
command = 'cat >> log.txt'

import antenna

antenna.listen(profile, queue_name, command)