
const findParentFolder = (folders, parentId) => folders.find(f => f.id === parentId);

const constructPath = (folder, allFolders) => {
  const pathSegments = [];
  let currentFolder = folder;

  while (currentFolder.parent_id !== null) {
    pathSegments.unshift(currentFolder.name);
    currentFolder = findParentFolder(allFolders, currentFolder.parent_id);
    if (!currentFolder) break;
  }

  pathSegments.unshift(currentFolder.name);
  return pathSegments.join('/');
};

export default constructPath;