import type { LayoutData } from './$types';
export const load = async ({ locals }) => {
	return {
		user: locals.user
	};
};
