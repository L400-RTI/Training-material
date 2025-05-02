# Training-material

These are only quick links to the chapters

1. [Introduction to RTI](./modules/01%20-%20Introduction.md) (Frank)
2. [Real-Time Hub](./modules/02%20-%20Real-Time%20Hub.md) (Matt)
3. [Connectors](./modules/03%20-%20Connectors.md) (Brian)
4. [Ingestion](./modules/04%20-%20Ingestion.md) (Brian)
5. [Data modelling](./modules/05%20-%20Data%20modelling.md) (Frank)
6. [Analytics](./modules/06%20-%20Analytics.md) (Brian)
7. [AI + Copilot](./modules/07%20-%20AI%20+%20Copliot.md) (Matt)
8. [Dashboards](./modules/08%20-%20Dashboards.md) (Matt)
9. [Rules (Activator)](#module-9---rules-activator) (Frank)
10. [Security](./modules/10%20-%20Security.md) (Matt)
11. [Networking](./modules/11%20-%20Networking.md) (Brian)
12. [CI/CD and ALM](./modules/12%20-%20CICD%20and%20ALM.md) (Frank)
13. [Appendix](./modules/13%20-%20Appendix.md) (all)

# Local Development Workflow

I was curios to see how our traning looks like, so I created a local development workflow that is able to serve the workshop right from your local computer. The prerequisits for this to run is that you have installed the **MOAW Cli** as described [here](https://moaw.dev/workshop/?src=create-workshop%2F&step=2#).

I added a simple PowerShell Script [here](./powershell/CombineMarkdown.ps1) that "compiles" (I know, I know 🤣) the different files into one single workshop file that you can find [here](./workshop.md).

To start the compilation please just call the PowerShell Script in the main directory of this project like

```powershell
.\powershell\CombineMarkdown.ps1
```

After the "compilation" is done you can start your local MOAW.dev instance with

```powershell
moaw serve '.\workshop.md'
```

| :heavy_exclamation_mark: **Important**                                                                                                                  |
| :------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **At the moment we have some problems with the path to the images. If someone knows how to solve this please let me know. I can code PowerShell then.** |
