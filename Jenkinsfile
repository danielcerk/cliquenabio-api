pipeline {
    agent any

    stages {

        stage ('Build Image') {
            steps {
                script {
                    dockerapp = docker.build('danielckgomes/api-cliquenabio', '-f ./src/Dockerfile ./src')
                    
                }
            }
        }
    }
}
