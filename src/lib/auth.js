const API_URL = 'http://localhost:8000/api';

export async function obtenerUsuarioActual() {
  try {
    const response = await fetch(`${API_URL}/me/`, {
      method: 'GET',
      credentials: 'include',
    });

    if (response.status === 401) {
      return null;
    }

    if (!response.ok) {
      throw new Error('No se pudo obtener el usuario actual.');
    }

    return await response.json();
  } catch (error) {
    console.error('Error al obtener usuario actual:', error);
    return null;
  }
}