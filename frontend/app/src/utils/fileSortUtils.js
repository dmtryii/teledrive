
const sortFiles = (files, criteria, order) => {
    const sortedFiles = [...files];
    sortedFiles.sort((a, b) => {
        if (criteria === 'name') {
            return order === 'asc' ? a.document_info.file_name.localeCompare(b.document_info.file_name) : b.document_info.file_name.localeCompare(a.document_info.file_name);
        } else if (criteria === 'size') {
            return order === 'asc' ? a.document_info.file_size - b.document_info.file_size : b.document_info.file_size - a.document_info.file_size;
        } else if (criteria === 'upload') {
            return order === 'asc' ? new Date(a.upload) - new Date(b.upload) : new Date(b.upload) - new Date(a.upload);
        }
        return 0;
    });
    return sortedFiles;
};
  
const filterFiles = (files, query) => {
    if (!query) return files;
    return files.filter(file => file.document_info.file_name.toLowerCase().includes(query.toLowerCase()));
};

const fileSortUtils = { sortFiles, filterFiles };

export default fileSortUtils;
