const ort = require('onnxruntime-web');
const fs = require('fs');

// Load the ONNX model
async function loadModel() {
    const modelBuffer = fs.readFileSync('random_forest_model.onnx');
    const session = await ort.InferenceSession.create(modelBuffer);
    return session;
}

// Make a prediction
async function makePrediction(session, data) {
    const input = new ort.Tensor('float32', Float32Array.from(data), [1, data.length]);
    const feeds = { float_input: input };
    const results = await session.run(feeds);
    return results.output.data;
}

// Example usage
(async () => {
    const session = await loadModel();
    const data = [ /* your feature values here */ ];
    const prediction = await makePrediction(session, data);
    console.log('Prediction:', prediction);
})();
