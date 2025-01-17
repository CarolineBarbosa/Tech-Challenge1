import pandas as pd
def get_table_name(opcao):
    if(opcao == "02"):
        table_name = 'BackupProducao'
    elif(opcao == "03"):
        table_name = 'BackupProcessaViniferas'
    elif(opcao == "04"):
        table_name = 'BackupComercio'
    elif(opcao == "05"):
        table_name = "BackupImpVinhos"
    elif(opcao == "06"):
        table_name = "BackupExpVinhos"
    return table_name

def get_columns(opcao, ano):
    if(opcao == "02" or opcao == "04"):
        fixed_columns= ['Produto']
        if ano is None:
            varied_columns = [f'`{year}`' for year in range(1970, 2024)]
        else:
            varied_columns =[f'`{ano}`']
        return (",".join(fixed_columns + varied_columns)),[x.lower() for x in fixed_columns]
    
    elif(opcao == "03"):
        fixed_columns= ['cultivar']
        if ano is None:
            varied_columns = [f'`{year}`'for year in range(1970, 2024)]
        else:
            varied_columns =[f'`{ano}`']
        return (",".join(fixed_columns + varied_columns)),[x.lower() for x in fixed_columns]
    
    elif(opcao == "05" or opcao == "06"):
        fixed_columns= ['País']
        if ano is None:
            varied_columns = [f'`{year}Quantidade`' for year in range(1970, 2024)]
            varied_columns2 = [f'`{year}Valor`' for year in range(1970, 2024)]
            
        else:
            varied_columns =[ f"`{ano}Quantidade`",f"`{ano}Valor`" ]
        return (",".join(fixed_columns + varied_columns)), [x.lower() for x in fixed_columns]

def display_data(df, opcao):
    data = []
    if opcao == "02" or opcao == "04":
        # Iterar sobre as linhas da tabela (exceto cabeçalhos)
        for row in range(len(df)):
            data.append({
                "Produto": df.loc[row, 'produto'],
                "Quantidade":  int(df.loc[row, 'Quantidade'] if pd.notna(df.loc[row, 'Quantidade']) else 0),  # Convert to native Python int
                "Ano": int(df.loc[row, 'Ano'] if pd.notna(df.loc[row, 'Ano']) else 0)   # Convert to native Python int
            })
    elif opcao == "03":
        # Iterar sobre as linhas da tabela (exceto cabeçalhos)
        for row in range(len(df)):
            data.append({
                "Cultivar": df.loc[row, 'cultivar'],
                "Quantidade_Kg":  int(df.loc[row, 'Quantidade'] if pd.notna(df.loc[row, 'Quantidade']) else 0),  # Convert to native Python int
                "Ano": int(df.loc[row, 'Ano'] if pd.notna(df.loc[row, 'Ano']) else 0)   # Convert to native Python int
            })
    elif opcao == "05" or opcao == "06":
        # Iterar sobre as linhas da tabela (exceto cabeçalhos)
        for row in range(len(df)):
            data.append({
                "País": df.loc[row, "País"],
                "Quantidade_Kg": int(df.loc[row, 'Quantidade'] if pd.notna(df.loc[row, 'Quantidade']) else 0), # Convert to native Python int
                "Valor": int(df.loc[row, 'Valor'] if pd.notna(df.loc[row, 'Valor']) else 0),  # Convert to native Python int
                "Ano":int(df.loc[row, 'Ano'] if pd.notna(df.loc[row, 'Ano']) else 0)  # Convert to native Python int
            })
    return data