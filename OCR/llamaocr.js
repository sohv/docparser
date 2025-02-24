import { ocr } from "llama-ocr";
import dotenv from "dotenv";

dotenv.config(); // Load environment variables from .env

async function runOCR() {
  try {
    const markdown = await ocr({
      filePath: "/Users/sohan/Documents/GitHub/docparser/images/figure-65.png", // Path to your image
      apiKey: process.env.TOGETHER_API_KEY, // API Key
    });

    console.log("OCR Result:\n", markdown);
  } catch (error) {
    console.error("❌ OCR failed:", error);
  }
}

// Run the function
runOCR();
