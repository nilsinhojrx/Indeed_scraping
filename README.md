# Indeed_scraping
Processo de web scraping que entra no Indeed e coleta as seguintes informações das vagas: 
- Cargo
- Empresa
- Localidade
- Link da Vaga
*****
O primeiro passo é realizar a pesquisa, manualmente, no site do Indeed, buscando as vagas desejadas.
Em seguida, pegue a URL após a pesquisa e coloque na função **main**. Dessa forma, o programa irá coletar as informações da primeira página, e, também, das páginas seguintes, até que não seja mais possível clicar no botão *próximo*. 
Por fim, os dados coletados serão salvos em um arquivo CSV, Excel,JSON, segundo as funções de salvamento do pacote **Pandas**.
*****
Os pacotes utilizados foram: Pandas, Parsel, Logging, Selenium

**Vídeo** : https://drive.google.com/file/d/1bhb2drIi_ANCVkU4u_m-bWwGfZcERZm8/view?usp=drive_link
