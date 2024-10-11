import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import requests
from datetime import datetime, time, date

class Dashboard:
    def __init__(self):
        self.layout()

    def layout(self):
        st.set_page_config(
            page_title="LiftOff",
            layout="wide",
            initial_sidebar_state="expanded")

        st.markdown("""
        <style>
        .big-font {
            font-size:80px !important;
        }
        </style>
        """, unsafe_allow_html=True)

        #Options Menu
        with st.sidebar:
            selected = option_menu('LiftOff', ["Home", 'Funcionário', 'Fornecedor', 'Produto', 'Vendas', 'Sobre'], 
                icons=['house', 'person-badge', 'truck', 'box', 'graph-up', 'info-circle'], menu_icon='intersect', default_index=0,
                styles={
                        "container": {"background-color": "#fafafa"},
                        "nav-link": {"--hover-color": "#eee"},
                        "nav-link-selected": {"background-color": "#0068C9"},
                    }
                )
            
        # Menu Lateral
        if selected=="Home":
            self.home()
        elif selected=="Funcionário":
            self.employee() 
        elif selected=="Fornecedor":
            self.supplier()     
        elif selected=="Produto":
            self.product()
        elif selected=="Vendas":
            self.sales()
        else:
            self.about() 

    def home(self):
        st.title('📊 LiftOff Data')
        st.subheader('Arquitetura de Pipeline de Dados Inovadora para Startups 🚀')

        st.divider()

        col1, col2 = st.columns([3, 2])
        with col1:
            st.header('Bem-vindo ao LiftOff Data')
            st.markdown(
                """
                Transforme sua startup com nossa solução de pipeline de dados de última geração!

                ### 🎯 Nossa Missão
                Capacitar startups com uma arquitetura de dados robusta, escalável e econômica, 
                permitindo que você se concentre no crescimento do seu negócio.

                ### 🔑 Principais Benefícios
                - **Economia**: Solução de baixo custo ideal para startups
                - **Eficiência**: Processamento e análise rápida de dados de vendas
                - **Escalabilidade**: Cresce com seu negócio
                - **Integração**: Conecta-se facilmente com APIs e CRMs existentes
                - **Colaboração**: Facilita o trabalho entre engenheiros e analistas de dados

                ### 🛠️ Nossa Tecnologia
                - Pipeline em camadas: Bronze, Silver e Gold
                - Kafka para streaming em tempo real
                - Airbyte para ingestão de dados flexível
                - Airflow para orquestração poderosa
                - DBT para transformações de dados confiáveis
                - Plataforma 'Briefer' para análise colaborativa
                """
            )
        with col2:
            st.image("https://www.scrapehero.com/wp/wp-content/uploads/2019/05/price-monitoring.gif", use_column_width=True)
            st.markdown("### 📈 Visualize seu Sucesso")
            st.metric(label="Aumento na Eficiência de Dados", value="300%", delta="50%")
            st.metric(label="Redução de Custos Operacionais", value="40%", delta="-15%")
            st.metric(label="Tempo de Insights", value="5 min", delta="-55 min")

        st.divider()
        st.subheader("Pronto para decolar? 🚀")
        if st.button("Agende uma Demo"):
            st.success("Obrigado pelo seu interesse! Nossa equipe entrará em contato em breve.")


    # Função auxiliar para exibir mensagens de erro detalhadas
    def show_response_message(self,response):
        if response.status_code == 200:
            st.success("Operação realizada com sucesso!")
        else:
            try:
                data = response.json()
                if "detail" in data:
                    # Se o erro for uma lista, extraia as mensagens de cada erro
                    if isinstance(data["detail"], list):
                        errors = "\n".join([error["msg"] for error in data["detail"]])
                        st.error(f"Erro: {errors}")
                    else:
                        # Caso contrário, mostre a mensagem de erro diretamente
                        st.error(f"Erro: {data['detail']}")
            except ValueError:
                st.error("Erro desconhecido. Não foi possível decodificar a resposta.")
    
    def product(self):
        st.title("Gerenciamento de Produtos")
        
        # Adicionar Produto
        with st.expander("Adicionar um Novo Produto"):
            with st.form("new_product"):
                name = st.text_input("Nome do Produto")
                description = st.text_area("Descrição do Produto")
                price = st.number_input("Preço", min_value=0.01, format="%f")
                categoria = st.selectbox(
                    "Categoria",
                    ["Eletrônico", "Eletrodoméstico", "Móveis", "Roupas", "Calçados"],
                )
                email_fornecedor = st.text_input("Email do Fornecedor")
                submit_button = st.form_submit_button("Adicionar Produto")

                if submit_button:
                    response = requests.post(
                        "http://backend:8000/products/",
                        json={
                            "name": name,
                            "description": description,
                            "price": price,
                            "categoria": categoria,
                            "email_fornecedor": email_fornecedor,
                        },
                    )
                    self.show_response_message(response)
        # Visualizar Produtos
        with st.expander("Visualizar Produtos"):
            if st.button("Exibir Todos os Produtos"):
                response = requests.get("http://backend:8000/products/")
                if response.status_code == 200:
                    product = response.json()
                    df = pd.DataFrame(product)

                    df = df[
                        [
                            "id",
                            "name",
                            "description",
                            "price",
                            "categoria",
                            "email_fornecedor",
                            "created_at",
                        ]
                    ]

                    # Exibe o DataFrame sem o índice
                    st.write(df.to_html(index=False), unsafe_allow_html=True)
                else:
                    self.show_response_message(response)

        # Obter Detalhes de um Produto
        with st.expander("Obter Detalhes de um Produto"):
            get_id = st.number_input("ID do Produto", min_value=1, format="%d")
            if st.button("Buscar Produto"):
                response = requests.get(f"http://backend:8000/products/{get_id}")
                if response.status_code == 200:
                    product = response.json()
                    df = pd.DataFrame([product])

                    df = df[
                        [
                            "id",
                            "name",
                            "description",
                            "price",
                            "categoria",
                            "email_fornecedor",
                            "created_at",
                        ]
                    ]

                    # Exibe o DataFrame sem o índice
                    st.write(df.to_html(index=False), unsafe_allow_html=True)
                else:
                    self.show_response_message(response)

        # Deletar Produto
        with st.expander("Deletar Produto"):
            delete_id = st.number_input("ID do Produto para Deletar", min_value=1, format="%d")
            if st.button("Deletar Produto"):
                response = requests.delete(f"http://backend:8000/products/{delete_id}")
                self.show_response_message(response)

        # Atualizar Produto
        with st.expander("Atualizar Produto"):
            with st.form("update_product"):
                update_id = st.number_input("ID do Produto", min_value=1, format="%d")
                new_name = st.text_input("Novo Nome do Produto")
                new_description = st.text_area("Nova Descrição do Produto")
                new_price = st.number_input(
                    "Novo Preço",
                    min_value=0.01,
                    format="%f",
                )
                new_categoria = st.selectbox(
                    "Nova Categoria",
                    ["Eletrônico", "Eletrodoméstico", "Móveis", "Roupas", "Calçados"],
                )
                new_email = st.text_input("Novo Email do Fornecedor")

                update_button = st.form_submit_button("Atualizar Produto")

                if update_button:
                    update_data = {}
                    if new_name:
                        update_data["name"] = new_name
                    if new_description:
                        update_data["description"] = new_description
                    if new_price > 0:
                        update_data["price"] = new_price
                    if new_email:
                        update_data["email_fornecedor"] = new_email
                    if new_categoria:
                        update_data["categoria"] = new_categoria

                    if update_data:
                        response = requests.put(
                            f"http://backend:8000/products/{update_id}", json=update_data
                        )
                        self.show_response_message(response)
                    else:
                        st.error("Nenhuma informação fornecida para atualização")

    def employee(self):
        st.title("Gerenciamento de Funcionários")

        # Adicionar Funcionário
        with st.expander("Adicionar um Novo Funcionário"):
            with st.form("new_employee"):
                first_name = st.text_input("Nome")
                last_name = st.text_input("Sobrenome")
                email = st.text_input("Email")
                phone_number = st.text_input("Número de Telefone")
                hire_date = st.date_input("Data de Contratação")
                department_id = st.number_input("ID do Departamento", min_value=1, step=1)
                job_title = st.text_input("Cargo")
                location = st.text_input("Localização")
                birth_date = st.date_input("Data de Nascimento")
                gender = st.selectbox("Gênero", ["Masculino", "Feminino", "Prefiro não dizer"])
                nationality = st.text_input("Nacionalidade")
                start_date = st.date_input("Data de Início")
                salary = st.number_input("Salário", min_value=0.01, format="%.2f")
                
                submit_button = st.form_submit_button("Adicionar Funcionário")

                if submit_button:
                    response = requests.post(
                        "http://backend:8000/employees/",
                        json={
                            "first_name": first_name,
                            "last_name": last_name,
                            "email": email,
                            "phone_number": phone_number,
                            "hire_date": hire_date.isoformat(),
                            "department_id": department_id,
                            "job_title": job_title,
                            "location": location,
                            "birth_date": birth_date.isoformat(),
                            "gender": gender,
                            "nationality": nationality,
                            "start_date": start_date.isoformat(),
                            "salary": salary
                        },
                    )
                    self.show_response_message(response)

        # Visualizar Funcionários
        with st.expander("Visualizar Funcionários"):
            if st.button("Exibir Todos os Funcionários"):
                response = requests.get("http://backend:8000/employees/")
                if response.status_code == 200:
                    employees = response.json()
                    df = pd.DataFrame(employees)
                    st.write(df.to_html(index=False), unsafe_allow_html=True)
                else:
                    self.show_response_message(response)

        # Obter Detalhes de um Funcionário
        with st.expander("Obter Detalhes de um Funcionário"):
            get_id = st.number_input("ID do Funcionário", min_value=1, format="%d")
            if st.button("Buscar Funcionário"):
                response = requests.get(f"http://backend:8000/employees/{get_id}")
                if response.status_code == 200:
                    employee = response.json()
                    df = pd.DataFrame([employee])
                    st.write(df.to_html(index=False), unsafe_allow_html=True)
                else:
                    self.show_response_message(response)

        # Deletar Funcionário
        with st.expander("Deletar Funcionário"):
            delete_id = st.number_input("ID do Funcionário para Deletar", min_value=1, format="%d")
            if st.button("Deletar Funcionário"):
                response = requests.delete(f"http://backend:8000/employees/{delete_id}")
                self.show_response_message(response)

        # Atualizar Funcionário
        with st.expander("Atualizar Funcionário"):
            with st.form("update_employee"):
                update_id = st.number_input("ID do Funcionário", min_value=1, format="%d")
                new_first_name = st.text_input("Novo Nome")
                new_last_name = st.text_input("Novo Sobrenome")
                new_email = st.text_input("Novo Email")
                new_phone_number = st.text_input("Novo Número de Telefone")
                new_department_id = st.number_input("Novo ID do Departamento", min_value=1, step=1)
                new_job_title = st.text_input("Novo Cargo")
                new_location = st.text_input("Nova Localização")
                new_gender = st.selectbox("Novo Gênero", ["Masculino", "Feminino", "Prefiro não dizer"])
                new_nationality = st.text_input("Nova Nacionalidade")
                new_start_date = st.date_input("Nova Data de Início")
                new_salary = st.number_input("Novo Salário", min_value=0.01, format="%.2f")
                new_termination_date = st.date_input("Nova Data de Término (opcional)")

                update_button = st.form_submit_button("Atualizar Funcionário")

                if update_button:
                    update_data = {}
                    if new_first_name:
                        update_data["first_name"] = new_first_name
                    if new_last_name:
                        update_data["last_name"] = new_last_name
                    if new_email:
                        update_data["email"] = new_email
                    if new_phone_number:
                        update_data["phone_number"] = new_phone_number
                    if new_department_id:
                        update_data["department_id"] = new_department_id
                    if new_job_title:
                        update_data["job_title"] = new_job_title
                    if new_location:
                        update_data["location"] = new_location
                    if new_gender:
                        update_data["gender"] = new_gender
                    if new_nationality:
                        update_data["nationality"] = new_nationality
                    if new_start_date:
                        update_data["start_date"] = new_start_date.isoformat()
                    if new_salary:
                        update_data["salary"] = new_salary
                    if new_termination_date:
                        update_data["termination_date"] = new_termination_date.isoformat()

                    if update_data:
                        response = requests.put(
                            f"http://backend:8000/employees/{update_id}", json=update_data
                        )
                        self.show_response_message(response)
                    else:
                        st.error("Nenhuma informação fornecida para atualização")

    def supplier(self):
        st.title("Gerenciamento de Fornecedores")
    
    def sales(self):
        st.title("Gerenciamento de Vendas")
        
        # Adicionar Venda
        with st.expander("Adicionar uma Nova Venda"):
            with st.form("new_sale"):
                email = st.text_input("Email do Vendedor")
                data = st.date_input("Data da compra", datetime.now())
                hora = st.time_input("Hora da compra", value=time(9, 0))
                valor = st.number_input("Valor da venda", min_value=0.0, format="%.2f")
                quantidade = st.number_input("Quantidade de produtos", min_value=1, step=1)
                produto = st.selectbox("Produto", options=["ZapFlow com Gemini", "ZapFlow com chatGPT", "ZapFlow com Llama3.0"])
                
                submit_button = st.form_submit_button("Adicionar Venda")

                if submit_button:
                    data_hora = datetime.combine(data, hora)
                    response = requests.post(
                        "http://backend:8000/sales/",
                        json={
                            "email": email,
                            "data": data_hora.isoformat(),
                            "valor": valor,
                            "quantidade": quantidade,
                            "produto": produto,
                        },
                    )
                    self.show_response_message(response)

        # Visualizar Vendas
        with st.expander("Visualizar Vendas"):
            if st.button("Exibir Todas as Vendas"):
                response = requests.get("http://backend:8000/sales/")
                if response.status_code == 200:
                    sales = response.json()
                    df = pd.DataFrame(sales)
                    st.write(df.to_html(index=False), unsafe_allow_html=True)
                else:
                    self.show_response_message(response)

        # Obter Detalhes de uma Venda
        with st.expander("Obter Detalhes de uma Venda"):
            get_id = st.number_input("ID da Venda", min_value=1, format="%d")
            if st.button("Buscar Venda"):
                response = requests.get(f"http://backend:8000/sales/{get_id}")
                if response.status_code == 200:
                    sale = response.json()
                    df = pd.DataFrame([sale])
                    st.write(df.to_html(index=False), unsafe_allow_html=True)
                else:
                    self.show_response_message(response)

        # Deletar Venda
        with st.expander("Deletar Venda"):
            delete_id = st.number_input("ID da Venda para Deletar", min_value=1, format="%d")
            if st.button("Deletar Venda"):
                response = requests.delete(f"http://backend:8000/sales/{delete_id}")
                self.show_response_message(response)

        # Atualizar Venda
        with st.expander("Atualizar Venda"):
            with st.form("update_sale"):
                update_id = st.number_input("ID da Venda", min_value=1, format="%d")
                new_email = st.text_input("Novo Email do Vendedor")
                new_data = st.date_input("Nova Data da compra")
                new_hora = st.time_input("Nova Hora da compra")
                new_valor = st.number_input("Novo Valor da venda", min_value=0.0, format="%.2f")
                new_quantidade = st.number_input("Nova Quantidade de produtos", min_value=1, step=1)
                new_produto = st.selectbox("Novo Produto", options=["ZapFlow com Gemini", "ZapFlow com chatGPT", "ZapFlow com Llama3.0"])

                update_button = st.form_submit_button("Atualizar Venda")

                if update_button:
                    update_data = {}
                    if new_email:
                        update_data["email"] = new_email
                    if new_data and new_hora:
                        update_data["data"] = datetime.combine(new_data, new_hora).isoformat()
                    if new_valor > 0:
                        update_data["valor"] = new_valor
                    if new_quantidade > 0:
                        update_data["quantidade"] = new_quantidade
                    if new_produto:
                        update_data["produto"] = new_produto

                    if update_data:
                        response = requests.put(
                            f"http://backend:8000/sales/{update_id}", json=update_data
                        )
                        self.show_response_message(response)
                    else:
                        st.error("Nenhuma informação fornecida para atualização")
    
    def about(self):
        st.title('Sobre o Projeto LiftOff Data')
        
        st.header('Arquitetura do Projeto')
        st.markdown("""
        Este projeto apresenta uma arquitetura de pipeline de dados inovadora e de baixo custo, projetada especificamente para startups. Nosso foco é na integração eficiente de dados de vendas provenientes de diversas fontes, como APIs e CRMs.

        ### Principais Características:
        - **Escalabilidade:** Solução adaptável ao crescimento da sua startup
        - **Eficiência:** Otimizada para ingestão, transformação e visualização de dados
        - **Colaboração:** Facilita o trabalho conjunto entre engenheiros e analistas de dados

        ### Componentes Chave:
        1. Pipeline em camadas: Bronze, Silver e Gold
        2. Integração com APIs
        3. Kafka para streaming de dados
        4. Airbyte para ingestão de dados
        5. Airflow para orquestração de tarefas
        6. DBT para transformação de dados
        7. Plataforma 'Briefer' para acesso e utilização dos dados transformados
        """)

        st.image("https://raw.githubusercontent.com/tsffarias/LiftOff_Data/refs/heads/main/img/arquitetura.png", use_column_width=True, caption="Arquitetura do Pipeline de Dados")

        st.divider()

        st.header('Sobre o Criador')
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### Thiago Silva Farias
            - 🎓 **Formação:** Sistemas de Informação - UFMS
            - 💼 **Experiência:** Engenheiro de Dados
            - 🔗 **LinkedIn:** [Perfil Profissional](https://www.linkedin.com/in/thiagosilvafarias/)
            - 📁 **GitHub:** [Repositório do Projeto](https://github.com/tsffarias/LiftOff_Data/tree/main)

            Obrigado por visitar o projeto LiftOff Data! Estou sempre aberto para discussões sobre engenharia de dados, arquiteturas de pipeline e tecnologias inovadoras. Não hesite em entrar em contato para trocar ideias ou colaborar em projetos futuros.
            """)

        with col2:
            st.image("https://www.scrapehero.com/wp/wp-content/uploads/2019/05/api-gif.gif", use_column_width=True, caption="Integração de Dados em Ação")

        
        
        

if __name__ == "__main__":
    Dashboard()