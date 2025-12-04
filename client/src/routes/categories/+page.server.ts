import type { PageServerLoad } from './$types';
import { env } from '$env/dynamic/public';

export const load: PageServerLoad = async ({ fetch }) => {
	const res = await fetch(`${env.PUBLIC_API_URL}/categories/`);
	const categories = await res.json();
	return {
		categories
	};
};
