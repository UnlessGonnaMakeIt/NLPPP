import { MongoClient } from 'mongodb';

const uri = process.env.MONGODB_URI;
const client = new MongoClient(uri);

export default async function handler(req, res) {
    if (req.method === 'POST') {
        const { category, english, chinese } = req.body;

        try {
            await client.connect();
            const db = client.db('dictionary');
            const collection = db.collection('entries');
            await collection.insertOne({ category, english, chinese });

            res.status(200).json({ message: 'Entry added successfully!' });
        } finally {
            await client.close();
        }
    } else {
        res.status(405).json({ message: 'Method not allowed' });
    }
}