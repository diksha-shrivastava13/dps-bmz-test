from llama_index.core import VectorStoreIndex
from pydantic_models import OutputSchema


async def extract_metadata(docs):
    try:
        index = VectorStoreIndex.from_documents(docs)
        query_engine = index.as_query_engine()

        answer = query_engine.query(
            f"""
            Your task is to go through the documents provided and determine the [country, project, program, theme, year,
            risk, severity and status] fields for the documents. These are clearly mentioned in the report. You must
            retrieve them by following the steps given below. 
            
            Step 1 - Extraction: Extract these sections out of the Kurzbeschreibung table: [country, 
            program (EZ_Programm), project, core_area (kernthema in the reports), year (year of the report in 
            Berichtszeitraum)]. Extract the value which comes after EZ_Programm  in the Kurzbeschreibung as the program
            field. Extract the value which comes afterKernthema in the Kurzbeschreibung as the theme. Extract  
            Berichtszeitraum year as the year field. Rely on the Kurzbeschreibung for the kernthema field. Return 
            "not specified" if not found. You can use the year specified in the file name to fill the year field.

            Step 2 - Status: Add project completion status by comparing the current month and year to the completion
            date specified in Berichtszeitraum. The dates in the document are specified as month/year format.
            "Maßnahme_im_Zeitplan" field from the document may be used for determining status.

            Step 3 - Risk: Determine if the project is at risk in yes/no by analysing the data in all sections of 
            the report including "4. Zielerreichung und Veränderungen der Risiken" and "Risikoeinschätzung" field of
            "Kurzbeschreibung". Make a field for at_risk and severity and specify if the risk is low, moderate or high.

            Step 4: Using the above instructions, return the answer in json format for the fields. Below is an example:
                country: str
                project: str
                program: str
                theme: str
                year: str
                risk: str
                severity: str
                status: str
                
            Step 5: Make sure the response is always within ``` ``` markers.
            """
        )
        return OutputSchema(summary="", fixed_data=str(answer.response))

    except Exception as e:
        return {"detail": f"Error processing {e}"}
