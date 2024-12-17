import json
import boto3
from datetime import datetime

def get_volume_id_from_arn(volume_arn):
    # Split the ARN using the colon (':') separator
    arn_parts = volume_arn.split(':')
    # The volume ID is the last part of the ARN after the 'volume/' prefix
    volume_id = arn_parts[-1].split('/')[-1]
    return volume_id

def lambda_handler(event, context):
    # Retrieve the volume ARN from the event input
    volume_arn = event['resources'][0]
    volume_id = get_volume_id_from_arn(volume_arn)

    # Create an EC2 client using boto3
    ec2_client = boto3.client('ec2')

    try:
        # Modify the volume to change its type (e.g., to 'gp3')
        response = ec2_client.modify_volume(
            VolumeId=volume_id,
            VolumeType='gp3'  # Adjust according to your needs
        )

        # Convert the datetime objects in the response to strings
        def convert_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()  # Convert datetime to ISO string
            raise TypeError("Type not serializable")

        # Convert the response to JSON-safe format
        response_json = json.dumps(response, default=convert_datetime)

        print(f"Volume ID: {volume_id}")  # Print the volume ID for debugging
        print(f"Modify volume response: {response_json}")  # Log the response for debugging

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f"Volume {volume_id} modified successfully",
                'response': response_json
            })
        }

    except Exception as e:
        # If there was an error modifying the volume, return the error message
        print(f"Error modifying volume {volume_id}: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f"Error modifying volume {volume_id}",
                'error': str(e)
            })
        }
