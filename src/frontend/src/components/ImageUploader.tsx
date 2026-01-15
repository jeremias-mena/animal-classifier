import React, { useState } from "react";
import { predictImage } from "../services/api";
import { normalizeImage } from "../utils/normalizeImage";

type PredictionResponse = {
    prediction: string;
    probabilities: Record<string, number>;
}

export default function ImageUploader() {
    const [file, setFile] = useState<File | null>(null);
    const [preview, setPreview] = useState<string | null>(null);
    const [result, setResult] = useState<PredictionResponse | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null)

    const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const selected = e.target.files?.[0];
        if (!selected) return;

        const isImage = selected.type.startsWith("image/") || /\.(jpe?g|png|webp)$/i.test(selected.name)

        if (!isImage){
            setError("Archivo inválido")
            return
        }

        if (selected.size > 10 * 1024 * 1024) {
            setError("Imagen demasiado pesada")
            return
        }

        try {
            const normalized = await normalizeImage(selected)
            setFile(selected);
            setPreview(normalized);
            setResult(null)
        } catch {
            setError("No se pudo procesar la imagen")
        }
        
    };

    const handlePredict = async () => {
        if (!file) return;

        console.log(file)
        console.log(file instanceof File)
        console.log(file.type)

        setLoading(true);
        try {
            const res = await predictImage(file);
            setResult(res);
        } catch (err) {
            console.error(err);
            alert("Error during prediction");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-md mx-auto p-6 bg-white rounded-xl shadow">
            <h1 className="text-2xl font-bold mb-4 text-center">
                Animal-Classifier
            </h1>

            <input 
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                className="block w-full text-sm text-gray-500 file:mr-4 
                          file:rounded-lg file:border-0
                          file:bg-blue-50 file:px-4 file:py-2
                          file:text-blue-700 hover:file:bg-blue-100"
                />
            
            <div className="w-72 h-72 rounded-xl border border-dashed border-gray-300 flex items-center justify-center overflow-hidden bg-gray-50">
                {preview ? (
                    <img src={preview} 
                         alt="preview" 
                         className="max-w-full max-h-full object-contain"
                         />
                ) : (
                    <span className="text-sm tex-gray-400">
                        Sin imagen
                    </span>
                )}
            </div>

            <button 
                onClick={handlePredict} 
                disabled={!file || loading}
                className="w-full bg-blue-600 text-white py-2 rounded disabled:opacity-50"
                >
                {loading ? "Predicting..." : "Predict"}
            </button>
            
            {error && (
                <p className="text-sm text-red-500">{error}</p>
            )}

            {result && (
                <div className="mt-4 text-center">
                    <p className="text-xl font-semibold">
                        Prediction: {result.prediction}
                    </p>
                    <div className="mt-2">
                        {Object.entries(result.probabilities).map(([cls, prob]) => (
                            <p key={cls}>
                                {cls}: {(prob * 100).toFixed(2)}%
                            </p>
                        ))}
                    </div>
                </div>
            )}

        </div>
    )
}