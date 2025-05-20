pip install ms-fabric-cli

$tenant_id="2c88391d-71ce-46fd-bcb4-50aad62f6198"
$capacity_id="A3CF09EC-4845-4191-9075-471B91289451"
$capacity_name = "dcodebifabric"
$workspace_name="RTIL400Tutorial"

# Login to Fabric CLI
# The tenant_id is the ID of the Azure AD tenant where your Fabric workspace is located.
# You can find this ID in the Azure portal under Azure Active Directory > Properties.
fab auth login

$_workspace_name="$($workspace_name).Workspace"
$_eventhouse_name="RTIL400.Eventhouse"
$_kql_db_name="RTIL400.KQLDatabase"
$_eventstream_name="RTIL400Eventstream.Eventstream"
$_kql_querysets_name=("RTIL400QuerySet.KQLQueryset","Tutorial_queryset.KQLQueryset")

# Create a new Fabric workspace
fab create $_workspace_name -P capacityname=$capacity_name 
fab set $_workspace_name -q description -i "This workspace is used for the RTI L400 training" -f

# Create a new Eventhouse
fab create $_workspace_name/$_eventhouse_name


