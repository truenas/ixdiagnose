## Building TrueNAS iXdiagnose

Prerequisites
- git
- pip

Step 1:
: Clone the **iXdiagnose** repository:
: `git clone https://github.com/truenas/ixdiagnose.git`

Step 2:
: Navigate to **iXdiagnose** directory. for example:
: `cd path/to/ixdiagnose`

Step 3: 
: Install dependencies:
: `pip install -r requirements.txt`

Step 4:
: Install the **iXdiagnose**:
: `python setup.py install`

step 5:
: The **iXdiagnose** application should now be installed and ready to use. You can run it and generate debug using the following command:
: `ixdiagnose run --debug-path="specify/path/to/debug"`
