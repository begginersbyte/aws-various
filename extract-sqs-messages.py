import boto3
#pip install boto3

def receive_messages(queue_url, file_path, max_messages=10, wait_time=10):
    # Initialize the boto3 client for SQS with hardcoded credentials
    sqs = boto3.client(
        'sqs',
        aws_access_key_id='<ACCESS KEY>',
        aws_secret_access_key='<SECRET KEY>',
        region_name='us-east-1' # whatever region is being used
    )

    try:
        # Open the file in append mode
        with open(file_path, "a", encoding="utf-8") as file:
            # Receive messages from the SQS queue
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=wait_time,
            )

            # Check if 'Messages' key is in the response
            if 'Messages' not in response:
                print("No messages available in the queue.")
                return []

            messages = response['Messages']

            for message in messages:
                # Process the message
                message_id = message['MessageId']
                receipt_handle = message['ReceiptHandle']
                body = message['Body']

                # Write the message details to the file
                file.write(f"Message ID: {message_id}\n")
                file.write(f"Receipt Handle: {receipt_handle}\n")
                file.write(f"Body: {body}\n")
                file.write("\n" + "="*40 + "\n\n")

                # After processing the message, delete it from the queue
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=receipt_handle
                )
                print(f"Deleted message ID: {message_id}")

            return messages

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
if __name__ == "__main__":
    QUEUE_URL = '<URL QUEUE>'
    FILE_PATH = "C:\\Users\\kevin\\Desktop\\output.txt"
    received_messages = receive_messages(QUEUE_URL, FILE_PATH)
