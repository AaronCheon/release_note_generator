pipeline{
    agent {
        label 'sun'
    }

    stages{
        stage("Setup Environment"){
            steps {
                //sh "printenv"
                sh "rm -rf ${env.gitlabSourceRepoName}; git clone ${env.gitlabSourceRepoURL}"
            }
        }
        stage("Release"){
            steps{script{
                def tag = env.gitlabBranch.replace("refs/tags/", "")
                echo "$tag"
                withCredentials([string(credentialsId: 'Jira-jenkins-token', variable: 'jira'), string(credentialsId: 'gitlabToken', variable: 'gitlab')]) {
                    sh "module load python/python/3.7.1; python3 mainFlow.py --link ${env.gitlabSourceRepoURL} --tag=${tag} --jira_token=${jira} --gitlab_token=${gitlab} --project_json ${env.gitlabSourceRepoName}/jenkins/releaseData.json --html_jinja ${env.gitlabSourceRepoName}/jenkins/emailSend.html.jinja --option=full"
                }
            }}
        }
    }
}
