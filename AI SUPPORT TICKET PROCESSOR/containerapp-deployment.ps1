$ContainerAppName = "ai-support-app"
$ResourceGroup = "ai-103-prac"
$EnvironmentName = "ai-200-containerapp-env"
$RegistryName = "a200raj"
$RegistryServer="a200raj.azurecr.io"
$FrontendImage = "$RegistryServer/support-frontend:v1"
$IdentityName = "ai200-acr-pull"

$IdentityId = az identity show `
    --name $IdentityName `
    --resource-group $ResourceGroup `
    --query id `
    --output tsv

az containerapp create `
    --name $ContainerAppName `
    --resource-group $ResourceGroup `
    --environment $EnvironmentName `
    --image $FrontendImage `
    --container-name support-frontend `
    --ingress external `
    --target-port 8000 `
    --user-assigned $IdentityId `
    --registry-server $RegistryServer `
    --registry-identity $IdentityId `
    --env-vars "BACKEND_URL=http://localhost:8001" `
    --cpu 0.25 `
    --memory 0.5Gi `
    --min-replicas 1 `
    --max-replicas 3