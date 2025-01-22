import { MongoClient } from 'mongodb';
import ExcelJS from 'exceljs';

const uri = process.env.MONGODB_URI;
const client = new MongoClient(uri);

export default async function handler(req, res) {
    try {
        await client.connect();
        const db = client.db('dictionary');
        const collection = db.collection('entries');

        // 获取所有词条
        const entries = await collection.find().toArray();

        // 创建 Excel 文件
        const workbook = new ExcelJS.Workbook();
        const worksheet = workbook.addWorksheet('Dictionary');
        worksheet.columns = [
            { header: 'English', key: 'english', width: 30 },
            { header: 'Chinese', key: 'chinese', width: 30 },
            { header: 'Category', key: 'category', width: 20 }
        ];

        // 添加数据到 Excel
        entries.forEach(entry => {
            worksheet.addRow({
                english: entry.english,
                chinese: entry.chinese,
                category: entry.category
            });
        });

        // 生成 Excel 文件
        const buffer = await workbook.xlsx.writeBuffer();

        // 设置响应头
        res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
        res.setHeader('Content-Disposition', 'attachment; filename=dictionary.xlsx');
        res.send(buffer);
    } catch (error) {
        res.status(500).json({ message: 'Error generating Excel file', error: error.message });
    } finally {
        await client.close();
    }
}