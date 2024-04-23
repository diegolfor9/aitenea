import streamlit as st
import pandas as pd
from rdkit import Chem
from rdkit.Chem import PandasTools

def load_data(uploaded_file):
    # Cargar datos sin agregar una columna de índice adicional
    df = pd.read_csv(uploaded_file)
    return df

def display_molecules(df):
    df['mol'] = df['SMILES'].apply(lambda x: Chem.MolFromSmiles(x))

    # Asegurarse de usar el índice del DataFrame como parte de la leyenda
    df['legend'] = df.index.astype(str) + ": " + df['SMILES']
    if 'Docking Scores' in df.columns:
        df['legend'] += "\nDocking Score: " + df['Docking Scores'].astype(str)
    
    img = PandasTools.FrameToGridImage(df, column='mol', legendsCol='legend', molsPerRow=3, subImgSize=(300, 300))
    return img

def main():
    st.title('Visualizador de Moléculas')
    uploaded_file = st.file_uploader("Cargue su archivo CSV", type=['csv'])

    if uploaded_file is not None:
        data = load_data(uploaded_file)
        if 'SMILES' in data.columns:
            # Se muestra el DataFrame sin el índice reseteado para evitar duplicaciones
            st.dataframe(data)
            img = display_molecules(data)
            st.image(img)
        else:
            st.error("El archivo CSV debe contener una columna 'SMILES'.")

if __name__ == "__main__":
    main()

