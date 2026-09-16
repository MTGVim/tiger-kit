// The consuming repository does not own menu data or its hierarchy.
export type Menu = { title: string; path: string; children?: Menu[] };
export async function loadMenus(): Promise<Menu[]> {
  return fetch('/api/session/navigation').then(response => response.json());
}
export function menuLink(menu: Menu) {
  return { text: menu.title, href: menu.path, children: menu.children?.map(menuLink) };
}
export const routes = { '/settlements/pending': { title: 'Waiting for approval' } };
