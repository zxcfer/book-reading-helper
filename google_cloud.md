# Bookie

## How this work

-  

## Setup

### firebase project

npm install -g firebase-tools
firebase login
firebase projects:list
firebase deploy --project nami-3210

### google cloud setup

gcloud functions deploy upload_book --trigger-bucket=img_out --runtime python37
gcloud functions logs read upload_book

https://console.firebase.google.com/u/0/project/nami-3210/functions/logs?functionFilter=upload_book(us-central1)&severity=DEBUG

https://googleapis.github.io/google-cloud-python/latest/storage/blobs.html

https://console.cloud.google.com/storage/browser/img_out?project=nami-3210

https://rominirani.com/google-cloud-functions-tutorial-using-the-cloud-scheduler-to-trigger-your-functions-756160a95c43

https://github.com/python-telegram-bot/python-telegram-bot

### Deploy and Test

1. Follow the [Cloud Functions quickstart guide][quickstart] to setup Cloud
Functions for your project.

1. Clone this repository:


        git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
        cd python-docs-samples/functions/imagemagick

1. Create a Cloud Storage Bucket:

        gsutil mb gs://YOUR_INPUT_BUCKET_NAME
        gsutil mb gs://YOUR_OUTPUT_BUCKET_NAME

     This second storage bucket is used to store blurred images. (Un-blurred images will not be saved to this bucket.)

1. Deploy the `blur_offensive_images` function with a Storage trigger:

        gcloud functions deploy blur_offensive_images --trigger-bucket=YOUR_INPUT_BUCKET_NAME --set-env-vars BLURRED_BUCKET_NAME=YOUR_OUTPUT_BUCKET_NAME --runtime python37

    * Replace `YOUR_INPUT_BUCKET_NAME` and `YOUR_OUTPUT_BUCKET_NAME` with the names of the respective Cloud Storage Buckets you created earlier.

1.  Upload an offensive image to the Storage bucket, such as this image of
    a flesh-eating zombie: https://cdn.pixabay.com/photo/2015/09/21/14/24/zombie-949916_1280.jpg

1.  Check the logs for the `blur_offensive_images` function:

        gcloud functions logs read blur_offensive_images

[quickstart]: https://cloud.google.com/functions/quickstart

#