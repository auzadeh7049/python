import boto3
import time
# variables
aws_region='ca-central-1'
vpc_subnet='172.16.0.0/16'
vpc_name='vpc01-172-16-0-0'
priv_cidr='172.16.1.0/24'
priv_subnet_name='vpc01_priv_subnet-172-16-1-0'
pub_cidr='172.16.2.0/24'
pub_subnet_name='vpc01_pub_subnet-172-16-2-0'
igateway_name='vpc01_igateway01'
pub_rtbl_name='vpc01_pub_rtbl01'


# initialize ec2 client
ec2=boto3.client('ec2', region_name=aws_region)
print('initialize ec2 client...')
time.sleep(1)


# create a vpc with a name tag
vpc=ec2.create_vpc(
CidrBlock=vpc_subnet,
TagSpecifications=[{ 'ResourceType': 'vpc', 'Tags': [{ "Key": "Name", "Value": vpc_name }] }] )
print('create a vpc with a name tag...')
time.sleep(1)


# create a private subnet
priv_subnet=ec2.create_subnet(
AvailabilityZone=aws_region + 'b',
VpcId=vpc['Vpc']['VpcId'],
CidrBlock=priv_cidr,
TagSpecifications=[{ 'ResourceType': 'subnet', 'Tags': [{ "Key": "Name", "Value": priv_subnet_name }] }] )
print('create the private subnet...')
time.sleep(1)


# create a public subnet, allow auto-assign public ip for subnet
pub_subnet=ec2.create_subnet(
AvailabilityZone=aws_region + 'b',
VpcId=vpc['Vpc']['VpcId'],
CidrBlock=pub_cidr,
TagSpecifications=[{ 'ResourceType': 'subnet', 'Tags': [{ "Key": "Name", "Value": pub_subnet_name }] }] )
print('create the public subnet, allow auto-assign public ip...')
time.sleep(1)
ec2.modify_subnet_attribute(
SubnetId=pub_subnet['Subnet']['SubnetId'],
MapPublicIpOnLaunch={'Value': True})


# create an internet gateway
igateway=ec2.create_internet_gateway(
TagSpecifications=[{ 'ResourceType': 'internet-gateway', 'Tags': [{ "Key": "Name", "Value": igateway_name }] }] )
time.sleep(1)
ec2.attach_internet_gateway(VpcId=vpc['Vpc']['VpcId'], InternetGatewayId=igateway["InternetGateway"]["InternetGatewayId"])
print('create an internet gateway and attach it to the public subnet...')


# create a new routing table for internet access, and an explicit subnet association with the public subnet
pub_rtbl=ec2.create_route_table(
VpcId=vpc['Vpc']['VpcId'],
TagSpecifications=[{ 'ResourceType': 'route-table', 'Tags': [{ "Key": "Name", "Value": pub_rtbl_name }] }] )
time.sleep(1)
ec2.associate_route_table(
RouteTableId=pub_rtbl['RouteTable']['RouteTableId'],
SubnetId=pub_subnet['Subnet']['SubnetId'] )
print('create a new routing table for public internet access, and an explicit subnet association with the public subnet...')
time.sleep(1)




# create a default route to the internet gateway on the public subnet
ec2.create_route(
RouteTableId=pub_rtbl['RouteTable']['RouteTableId'],
DestinationCidrBlock='0.0.0.0/0',
GatewayId=igateway['InternetGateway']['InternetGatewayId'])
print('create a default route to the internet gateway on the public subnet...')
time.sleep(1)
