import { MongoClient, ObjectId } from 'mongodb';

const uri = process.env.MONGODB_URI;
const client = new MongoClient(uri);

export default async function handler(req, res) {
    if (req.method === 'DELETE') {
        const entryId = req.query.id;

        try {
            await client.connect();
            const db = client.db('dictionary');
            const collection = db.collection('entries');
            await collection.deleteOne({ _id: new ObjectId(entryId) });

            res.status(200).json({ message: 'Entry deleted successfully!' });
        } finally {
            await client.close();
        }
    } else {
        res.status(405).json({ message: 'Method not allowed' });
    }
}