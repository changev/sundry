node{
    def junitFiles = findFiles glob: 'RackHD/test/*.xml'
    boolean exists = junitFiles.length > 0
    if (exists){
      junit 'RackHD/test/*.xml'
      int failure_count = 0
      int error_count = 0
      if(fileExists ("downstream_file")) {
                                def props = readProperties file: "downstream_file"
                                failure_count = "${props.failures}".toInteger()
                                error_count = "${props.errors}".toInteger()
                            }
                            if (failure_count > 0 || error_count > 0){
                                currentBuild.result = "SUCCESS"
                                echo "there are failed test cases"
                                sh 'exit 1'
                            }
                        }
}
