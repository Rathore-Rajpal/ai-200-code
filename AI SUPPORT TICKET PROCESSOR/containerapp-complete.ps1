$ContainerAppName = "ai-support-app"
$ResourceGroup = "ai-103-prac"

$RegistryServer = "a200raj.azurecr.io"
$FrontendImage = "$RegistryServer/support-frontend:v1"
$BackendImage = "$RegistryServer/ai-backend:v2"

$IdentityName = "ai200-acr-pull"

$IdentityId = az identity show `
    --name $IdentityName `
    --resource-group $ResourceGroup `
    --query id `
    --output tsv


@"
identity:
  type: UserAssigned
  userAssignedIdentities:
    "$IdentityId": {}

properties:

  configuration:

    activeRevisionsMode: Single

    ingress:
      external: true
      allowInsecure: false
      targetPort: 8000
      transport: auto

    registries:
      - server: "$RegistryServer"
        identity: "$IdentityId"

  template:

    containers:

      - name: support-frontend
        image: "$FrontendImage"

        env:
          - name: BACKEND_URL
            value: "http://localhost:8001"

        resources:
          cpu: 0.25
          memory: 0.5Gi


      - name: ai-backend
        image: "$BackendImage"

        env:

          - name: OPENAI_BASE_URL
            value: "https://ai-200-raj01.openai.azure.com/openai/v1"

          - name: MODEL_DEPLOYMENT
            value: "gpt-4.1"

          - name: OPENAI_API_KEY
            secretRef: "apikey"

        resources:
          cpu: 0.5
          memory: 1Gi


    scale:
      minReplicas: 1
      maxReplicas: 3
"@ | Set-Content ./containerapp.yaml