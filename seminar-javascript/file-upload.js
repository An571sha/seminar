import { S3 } from 'aws-sdk';
import { PutObjectOutput } from 'aws-sdk/clients/s3';


const createS3Service = (s3 ) => {
  if(!s3) {
    throw new Error('s3 file system is not defined');
  }
  return {
    getObject: (params ) => new Promise((resolve, reject) => {
      s3.getObject(params, (err, data) => {
        if (err) {
          console.error(`S3 getObject has been failed for the file : ${params.Key} in bucket ${params.Bucket}.` );
          console.log(err);
          reject(err);
        } else {
          console.info(`S3 getObject was successful for file : ${params.Key}`);
          resolve(JSON.parse(data.Body.toString()));
        }
      });
    }),
    uploadObject: (params) => new Promise((resolve, reject) => {
      console.log('########### start s3 upload');
      s3.putObject(params, (err, data) => {
        if (err) {
          console.error(`S3 putObject has been failed for the file : ${params.Key} in bucket ${params.Bucket}.` );
          console.log(err);
          reject(err);
        } else {
          console.info(`S3 putObject was successful for file : ${params.Key}`);
          resolve({ status: 'success' });
        }
      });
    }),
  };
}

export default createS3Service;