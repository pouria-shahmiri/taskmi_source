# app.py

import streamlit as st
import pandas as pd

def main():
    st.title("TaskMi Source Modifier")

    # File Upload
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)

        # Display the current DataFrame
        st.dataframe(df)

        # Add a row
        if st.button("Add Row"):
            new_row = pd.Series([None] * len(df.columns), index=df.columns)
            df = df.append(new_row, ignore_index=True)
            st.dataframe(df)

        # Delete a row
        row_to_delete = st.number_input("Enter the row index to delete (0-based index)", min_value=0, max_value=len(df)-1, step=1, key='row_to_delete')
        if st.button("Delete Row"):
            df = df.drop(index=row_to_delete).reset_index(drop=True)
            st.dataframe(df)

        # Modify a row
        row_to_modify = st.number_input("Enter the row index to modify (0-based index)", min_value=0, max_value=len(df)-1, step=1, key='row_to_modify')
        st.write(f"Editing Row {row_to_modify + 1}")
        for col in df.columns:
            new_value = st.text_input(f"Enter new value for {col}", value=df.at[row_to_modify, col], key=f'{row_to_modify}_{col}')
            df.at[row_to_modify, col] = new_value

        st.dataframe(df)

        # Save the modified DataFrame back to Excel
        if st.button("Save Changes"):
            df.to_excel("modified_excel_file.xlsx", index=False)
            st.success("Changes saved successfully!")

        # Download the modified Excel file
        if st.button("Download Modified Excel"):
            with open("modified_excel_file.xlsx", "rb") as file:
                file_content = file.read()
                st.download_button(label="Download", data=file_content, file_name="modified_excel_file.xlsx", key="download_button")

if __name__ == "__main__":
    main()
