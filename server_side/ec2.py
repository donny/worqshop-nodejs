import boto
import time
import paramiko

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

DEFAULT_REGION = 'us-east-1'
DEFAULT_IMAGE = 'ami-e56e8f8c'
DEFAULT_KEY_NAME = 'worqshop'
DEFAULT_SECURITY_GROUP = 'worqshop'
DEFAULT_INSTANCE_TYPE = 'm1.small'
DEFAULT_AVAILABILITY_ZONE = 'us-east-1a'


conn = boto.connect_ec2(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

images = conn.get_all_images(image_ids=[DEFAULT_IMAGE])
image = images[0]

reservation = image.run(key_name=DEFAULT_KEY_NAME, security_groups=[DEFAULT_SECURITY_GROUP], instance_type=DEFAULT_INSTANCE_TYPE, placement=DEFAULT_AVAILABILITY_ZONE)

time.sleep(5)

instance = reservation.instances[0]

time.sleep(5)

while (instance.update() != 'running'):
	time.sleep(10)

print instance.dns_name


#ssh = paramiko.SSHClient()
#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#host = ''
#user = 'root'
#ssh.connect(host, username=user, key_filename='/home/donny/.ec2/worqshop.pem')
#stdin,stdout,stderr = ssh.exec_command('uptime')

