// Web版の経費精算システム - フロントエンド

import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import axios from 'axios';

const ExpenseSystem = () => {
  const [category, setCategory] = useState('飛行機');
  const [file, setFile] = useState(null);
  const [feedback, setFeedback] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!file) {
      alert('ファイルを選択してください。');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('category', category);

    try {
      const response = await axios.post('https://your-backend-url.onrender.com/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setFeedback(response.data.feedback);
    } catch (error) {
      console.error('エラーが発生しました。', error);
      setFeedback('エラーが発生しました。もう一度お試しください。');
    }
  };

  return (
    <div className="p-8">
      <Card className="p-4">
        <CardContent>
          <h1 className="text-xl mb-4">経費精算システム</h1>

          <div className="mb-4">
            <label>カテゴリを選択:</label>
            <select value={category} onChange={(e) => setCategory(e.target.value)} className="ml-2 p-2 border rounded">
              <option value="飛行機">飛行機</option>
              <option value="ホテル">ホテル</option>
              <option value="バス">バス</option>
            </select>
          </div>

          <div className="mb-4">
            <input type="file" accept=".png, .jpg, .jpeg, .pdf" onChange={handleFileChange} />
          </div>

          <Button onClick={handleSubmit}>ファイルをアップロード</Button>

          {feedback && (
            <div className="mt-4 p-4 border rounded bg-gray-100">
              <pre>{feedback}</pre>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default ExpenseSystem;
