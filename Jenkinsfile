pipeline {
    agent any
	
	environment {
        AWS_ACCESS_KEY_ID = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
        AWS_DEFAULT_REGION = 'us-east-1'
    }
	
	parameters {
        choice(name: 'Run_Build_Deploy', choices: ['Yes', 'No'], description: 'Run the Build & Deploy stage?', defaultValue: 'No')
		choice(name: 'Run_Pull_Test', choices: ['Yes', 'No'], description: 'Run the Pull & Test stage?', defaultValue: 'No')
    }
    
    stages {
        stage('Build & Deploy') {
		    when {
                expression { env.CHANGE_ID != null || params.Run_Build_Deploy == 'Yes' }
            }
            steps {
                sh 'docker build -t python-app .'
				sh 'docker run --name app-container python-app'
				sh 'docker cp app-container:/usr/app/artifact.txt .'
				sh 'aws s3 cp artifact.txt s3://piotrrespondek/artifact.txt'
				sh 'docker login -u AWS -p $(aws ecr get-login-password --region ${AWS_DEFAULT_REGION}) 161192472568.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com'
				sh 'docker tag python-app:latest 161192472568.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/piotrrespondek:latest'
				sh 'docker push 161192472568.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/piotrrespondek:latest'
            }
        }
        stage('Pull & Test') {
		    triggers {
                cron('H 3 * * *')
            }
			when {
                anyOf {
                    triggeredBy 'TimerTrigger'
                    expression { params.Run_Pull_Test == 'Yes' }
                }
            }
            steps {
                script {
					 def key = sh(
                        script: "aws s3 ls piotrrespondek --recursive | sort | tail -n 1 | awk '{print \$4}'",
                        returnStdout: true
                    ).trim()
					sh 'aws s3 cp s3://piotrrespondek/${key} .'
					def txtFile = findFiles(glob: '*.txt')
					def size = fileSize(${txtFile})
					if (size == 0) {
                            echo "The file is empty"
					}   
						else {
                            echo "The file is not empty"
                    }
				}
            }
        }
    }
}