from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
from io import BytesIO
import os
from main import segment_everything

app = FastAPI()

@app.post("/segment-image")
async def segment_image(file: UploadFile = File(...)):
    try:
        image_input = await file.read()

        # Converting bytes to PIL Image
        image = Image.open(BytesIO(image_input)).convert("RGB")

        # Calling the segment_everything function
        result = segment_everything(image=image)

        # Saving the result
        result_path = "generated/output.png"
        os.makedirs(os.path.dirname(result_path), exist_ok=True)
        result.save(result_path)

        return {"segmentation_result_path": result_path}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

