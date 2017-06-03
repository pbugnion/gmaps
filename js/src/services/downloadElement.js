import { html2canvas } from '../vendor/html2canvas'

const downloadElementAsPng = ($element, downloadName) => {
    return new Promise((resolve, reject) => {
        html2canvas($element, {
            useCORS: true,
            onrendered: (canvas) => {
                const a = document.createElement("a");
                a.download = downloadName;
                a.href = canvas.toDataURL("image/png");
                document.body.appendChild(a);
                a.click();
                resolve();
            },
            onerror: (error) => {
                reject(error);
            }
        })
    });
}

export { downloadElementAsPng };
