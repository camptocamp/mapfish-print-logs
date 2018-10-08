#!groovy
@Library('c2c-pipeline-library')
import static com.camptocamp.utils.*

final IMAGE_NAME = 'camptocamp/mapfish-print-logs'

// make sure we don't mess with another build by using latest on both
env.IN_CI = '1'

dockerBuild {
    stage('Update docker') {
        checkout scm
        sh 'make pull'
    }
    stage('Build') {
        checkout scm
        parallel 'Main': {
            sh 'make build'
        }, 'Tests': {
            sh 'make build_acceptance'
        }
    }
    stage('Test') {
        checkout scm
        try {
            lock("acceptance-${env.NODE_NAME}") {  //only one acceptance test at a time on a machine
                sh 'make acceptance'
            }
        } finally {
            junit keepLongStdio: true, testResults: 'reports/*.xml'
        }
    }

    if (env.BRANCH_NAME == 'master') {
        stage("Publish master") {
            checkout scm
            setCronTrigger('H H(18-23) * * *')
            //push them
            withCredentials([[$class          : 'UsernamePasswordMultiBinding', credentialsId: 'dockerhub',
                              usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']]) {
                sh 'docker login -u "$USERNAME" -p "$PASSWORD"'
                docker.image("${IMAGE_NAME}:latest").push()
                sh 'rm -rf ~/.docker*'
            }
        }
    }
}
