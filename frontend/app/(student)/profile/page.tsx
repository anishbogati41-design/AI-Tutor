"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ApiError, apiRequest } from "@/lib/api";
import type { AccessibilityPreferences, User } from "@/types/user";

const profileSchema = z.object({
  name: z.string().trim().min(1, "Enter your name").max(100),
  email: z.email("Enter a valid email address"),
});

const preferencesSchema = z.object({
  font_size: z.string().trim().min(1).max(32),
  readable_mode: z.boolean(),
  high_contrast: z.boolean(),
  dyslexia_mode: z.boolean(),
});

type ProfileValues = z.infer<typeof profileSchema>;
type PreferenceValues = z.infer<typeof preferencesSchema>;

export default function ProfilePage() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const currentUser = useQuery({
    queryKey: ["current-user"],
    queryFn: () => apiRequest<User>("/users/me"),
  });
  const profileForm = useForm<ProfileValues>({
    resolver: zodResolver(profileSchema),
  });
  const preferenceForm = useForm<PreferenceValues>({
    resolver: zodResolver(preferencesSchema),
  });

  useEffect(() => {
    if (currentUser.data) {
      profileForm.reset({
        name: currentUser.data.name,
        email: currentUser.data.email,
      });
      preferenceForm.reset({
        font_size: currentUser.data.font_size,
        readable_mode: currentUser.data.readable_mode,
        high_contrast: currentUser.data.high_contrast,
        dyslexia_mode: currentUser.data.dyslexia_mode,
      });
    }
  }, [currentUser.data, preferenceForm, profileForm]);

  useEffect(() => {
    if (currentUser.error instanceof ApiError && currentUser.error.status === 401) {
      router.replace("/login");
    }
  }, [currentUser.error, router]);

  const updateProfile = useMutation({
    mutationFn: (values: ProfileValues) =>
      apiRequest<User>("/users/me", {
        method: "PUT",
        body: JSON.stringify(values),
      }),
    onSuccess: (user) => queryClient.setQueryData(["current-user"], user),
  });

  const updatePreferences = useMutation({
    mutationFn: (values: PreferenceValues) =>
      apiRequest<AccessibilityPreferences>("/users/me/preferences", {
        method: "PUT",
        body: JSON.stringify(values),
      }),
    onSuccess: (preferences) => {
      queryClient.setQueryData<User | undefined>(
        ["current-user"],
        (user) => (user ? { ...user, ...preferences } : user),
      );
      router.push("/lessons");
    },
  });

  if (currentUser.isPending) {
    return <main className="p-8 text-slate-600">Loading your profile…</main>;
  }
  if (!currentUser.data) {
    return <main className="p-8 text-red-700">Unable to load your profile.</main>;
  }

  return (
    <AppShell>
      <div className="mx-auto max-w-4xl">
      <header>
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.16em] text-blue-700">
            Adaptive Education
          </p>
          <h1 className="mt-2 text-3xl font-bold">Profile and preferences</h1>
        </div>
      </header>

      <div className="mt-8 grid gap-6 md:grid-cols-2">
        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-bold">Account</h2>
          <form
            className="mt-5 space-y-4"
            onSubmit={profileForm.handleSubmit((values) =>
              updateProfile.mutate(values),
            )}
          >
            <div>
              <label htmlFor="profile-name" className="mb-2 block text-sm font-semibold">
                Name
              </label>
              <Input id="profile-name" {...profileForm.register("name")} />
              {profileForm.formState.errors.name && (
                <p className="mt-1 text-sm text-red-700">
                  {profileForm.formState.errors.name.message}
                </p>
              )}
            </div>
            <div>
              <label htmlFor="profile-email" className="mb-2 block text-sm font-semibold">
                Email
              </label>
              <Input
                id="profile-email"
                type="email"
                {...profileForm.register("email")}
              />
              {profileForm.formState.errors.email && (
                <p className="mt-1 text-sm text-red-700">
                  {profileForm.formState.errors.email.message}
                </p>
              )}
            </div>
            {updateProfile.error && (
              <p role="alert" className="text-sm text-red-700">
                {updateProfile.error instanceof ApiError
                  ? updateProfile.error.message
                  : "Unable to update the profile"}
              </p>
            )}
            {updateProfile.isSuccess && (
              <p role="status" className="text-sm text-green-700">
                Profile saved.
              </p>
            )}
            <Button type="submit" disabled={updateProfile.isPending}>
              Save profile
            </Button>
          </form>
        </section>

        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-bold">Accessibility</h2>
          <form
            className="mt-5 space-y-4"
            onSubmit={preferenceForm.handleSubmit((values) =>
              updatePreferences.mutate(values),
            )}
          >
            <div>
              <label htmlFor="font-size" className="mb-2 block text-sm font-semibold">
                Font size
              </label>
              <select
                id="font-size"
                className="min-h-11 w-full rounded-lg border border-slate-300 bg-white px-3"
                {...preferenceForm.register("font_size")}
              >
                <option value="default">Default</option>
                <option value="large">Large</option>
                <option value="extra-large">Extra large</option>
              </select>
            </div>
            {[
              ["readable_mode", "Readable mode"],
              ["high_contrast", "High contrast"],
              ["dyslexia_mode", "Dyslexia-friendly mode"],
            ].map(([name, label]) => (
              <label key={name} className="flex items-center gap-3">
                <input
                  type="checkbox"
                  className="size-5 accent-blue-700"
                  {...preferenceForm.register(name as keyof PreferenceValues)}
                />
                <span>{label}</span>
              </label>
            ))}
            {updatePreferences.error && (
              <p role="alert" className="text-sm text-red-700">
                Unable to save accessibility preferences.
              </p>
            )}
            {updatePreferences.isSuccess && (
              <p role="status" className="text-sm text-green-700">
                Preferences saved.
              </p>
            )}
            <Button type="submit" disabled={updatePreferences.isPending}>
              Save preferences and continue
            </Button>
          </form>
        </section>
      </div>
      </div>
    </AppShell>
  );
}
