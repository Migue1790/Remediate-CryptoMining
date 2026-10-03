import boto3
import os

ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')
sns = boto3.client('sns')

def lambda_handler(event, context):
    instance_id = event['detail']['resource']['instanceDetails']['instanceId']

    # Detiene la instancia
    ec2.stop_instances(InstanceIds=[instance_id])

    # Ejecuta comandos forenses
    ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName='AWS-RunShellScript',
        Parameters={
            'commands': [
                'uptime > /tmp/uptime.txt',
                'ps aux > /tmp/procs.txt',
                'netstat -tunap > /tmp/netstat.txt'
            ]
        }
    )

    # Envía notificación SNS
    sns.publish(
        TopicArn=os.environ['SNS_TOPIC_ARN'],
        Subject='Alerta de Cryptomining',
        Message=f'Se detectó tráfico Tor en la instancia {instance_id}. Se detuvo y se inició análisis forense.'
    )
