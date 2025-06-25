import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json'
    }
});

export default {
    uploadDocument(file) {
        const formData = new FormData();
        formData.append('file', file);
        return apiClient.post('/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
    },
    getAnswer(query) {
        return apiClient.get(`/qa?query=${query}`);
    }
};