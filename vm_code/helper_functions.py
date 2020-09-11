"""Helper function for GCP communication."""
import datetime
import os

def create_bucket(bucket_name):
    """Creates a new bucket."""
    create_command = "gsutil mb " + bucket_name
    os.system(create_command)

def upload_blob(bucket_name, uploads_dir):
    """Uploads files to the bucket."""
    upload_command = "gsutil -m cp -r " + uploads_dir + " " + bucket_name + "/audio"
    os.system(upload_command)        

def run_preprocessing(bucket_name, region):
    """Runs preprocessing job on AI Platform"""
    job_name = "preprocessing_job_" + str(int((datetime.datetime.now()-datetime.datetime(1970,1,1)).total_seconds()))
    config_file = os.path.join(os.getcwd(), "../magenta_docker/config_single_vm.yaml") 
    job_submission_command = (
        "gcloud ai-platform jobs submit training " + job_name +
        " --region " + region +
        " --config " + config_file +
        " --master-image-uri $PREPROCESSING_IMAGE_URI" +
        " -- " +
        " --input_audio_filepatterns=" + os.path.join(bucket_name, 'audio/*') +
        " --output_tfrecord_path=" + os.path.join(bucket_name, 'tf_record/train.tfrecord'))
    os.system(job_submission_command)

def submit_job(request, bucket_name, region):
    """Submit training job to AI Platform"""
    os.system("export PATH=/usr/local/google/home/$USER/.local/bin:$PATH")
    print(32)
    job_name = "training_job_" + str(int((datetime.datetime.now()-datetime.datetime(1970,1,1)).total_seconds()))
    print(34)
    config_file = os.path.join(os.getcwd(), "../magenta_docker/config_multiple_vms.yaml") 
    print(36)
    submitting_job = "gcloud ai-platform jobs submit training "\
    + job_name + " --region europe-west4"\
    + " --master-image-uri $IMAGE_URI"\
    + " --config " + config_file\
    + " -- --save_dir=" + bucket_name + "/model"\
    + " --file_pattern=" + bucket_name + "/tf_record" + "/train.tfrecord*"\
    + " --batch_size=" + str(request.form["batch_size"])\
    + " --learning_rate=" + str(request.form["learning_rate"])\
    + " --num_steps=" + str(request.form["num_steps"])\
    + " --steps_per_summary=" + str(request.form["steps_per_summary"])\
    + " --steps_per_save=" + str(request.form["steps_per_save"])\
    + " --early_stop_loss_value=" + str(request.form["early_stop_loss_value"])
    print("here before submit")
    os.system(submitting_job)
    print("here after submit")
    
    