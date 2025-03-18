function changeAccessory(accessory) {
    fetch(`/change_accessory?accessory=${accessory}`);
}
