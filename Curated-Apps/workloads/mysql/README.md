# Gramine Curated MySQL
In the following two sections, we explain how a Docker image for the protected MySQL version can
be built and how the image can be executed.
[Prerequisites](https://github.com/gramineproject/contrib/tree/master/Curated-Apps/README.md) for
both the phases are assumed to be met.

## Build a confidential compute image for MySQL
Execute the below commands on the VM.

1. Clone the Gramine Contrib repository and move to the Curated-Apps folder:
   ```sh
   git clone --depth 1 https://github.com/gramineproject/contrib.git
   cd contrib/Curated-Apps
   ```

2. Initialize MySQL database using below commands, skip this step if users want to use thier
   existing MySQL database:
   ```sh
   mkdir workloads/mysql/test_db
   docker run --rm --net=host --name init_test_db --user $(id -u):$(id -g) \
       -v $PWD/workloads/mysql/test_db:/test_db \
       -e MYSQL_ALLOW_EMPTY_PASSWORD=true -e MYSQL_DATABASE=test_db mysql:8.0.32-debian \
       --datadir /test_db &

   # Execute below command when mysql server is ready for connections after database initialization
   docker stop init_test_db
   ```

3. Encrypt MySQL database

   1. Install prerequisites for encrypting MySQL database

      [Install Gramine](https://gramine.readthedocs.io/en/latest/quickstart.html#install-gramine): Encryption is done using `gramine-sgx-pf-crypt` tool which is part of Gramine installation.

   2. Encrypt MySQL database following below steps:
      ```sh
      dd if=/dev/urandom bs=16 count=1 > workloads/mysql/encryption_key
      sudo rm -rf /var/run/test_db_encrypted
      sudo gramine-sgx-pf-crypt encrypt -w workloads/mysql/encryption_key \
          -i workloads/mysql/test_db -o /var/run/test_db_encrypted
      ```
      The above commands encrypts MySQL database `workloads/mysql/test_db` to
      `/var/run/test_db_encrypted` with encryption key `workloads/mysql/encryption_key`.
      Learn more about [Encrypted files](https://gramine.readthedocs.io/en/stable/manifest-syntax.html#encrypted-files) support in Gramine.

4. Generate the test confidential compute image based on the `mysql:8.0.32-debian` image as shown
      below:
      ```sh
      python3 ./curate.py mysql mysql:8.0.32-debian test
      ```

5. Or, to generate a custom confidential compute image based on a user-provided MySQL image,
   execute the following to launch an interactive setup script:
   ```sh
   python3 ./curate.py mysql <your_image>
   ```

## Run the confidential compute image for MySQL

- This example was tested on a Standard_DC8s_v3 Azure VM.
- Follow the output of the `curate.py` script to run the generated Docker image(s).

## Connect mysql client

   Install MySQL client using command:
   ```sh
   sudo apt-get -y install mysql-client
   ```

   Connect client to the MySQL server created using test confidential compute image using command
   ```sh
   mysql -h 127.0.0.0 -uroot
   ```

## Decrypt MySQL database

   Execute below command to decrypt the MySQL database:
   ```sh
   gramine-sgx-pf-crypt decrypt -w workloads/mysql/encryption_key \
       -i /var/run/test_db_encrypted -o test_db_plain
   ```

## Contents
This sub-directory contains artifacts which help in creating curated GSC MySQL image, as explained
below:

    .
    |-- mysql-gsc.dockerfile.template     # Template used by `curation_script.sh` to create a
    |                                       wrapper dockerfile `mysql-gsc.dockerfile` that
    |                                       includes user-provided inputs e.g. `ca.cert` file etc.
    |                                       into the graminized MySQL image.
    |-- mysql.manifest.template           # Template used by `curation_script.sh` to create a
    |                                       user manifest file (with basic set of values defined
    |                                       for graminizing MySQL images), that will be passed to
    |                                       GSC.