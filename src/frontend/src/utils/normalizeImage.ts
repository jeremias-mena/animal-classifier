export function normalizeImage(file: File, maxSize = 512): Promise<string> {
    return new Promise((resolve, reject) => {
        const img = new Image()
        const url = URL.createObjectURL(file)

        img.onload = () => {
            const scale = Math.min(maxSize / img.width, maxSize / img.height, 1)
            
            const canvas = document.createElement("canvas")
            canvas.width = img.width * scale
            canvas.height = img.height * scale

            const ctx = canvas.getContext("2d")
            if (!ctx) return reject()
            
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height)

            resolve(canvas.toDataURL("image/jpeg", 0.9))
            URL.revokeObjectURL(url)
        }

        img.onerror = reject
        img.src = url

    })
}