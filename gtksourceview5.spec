# TODO: use gtk4-update-icon-cache
#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
%bcond_with	sysprof		# sysprof profiler support
%bcond_without	vala		# do not build Vala API

Summary:	Text widget that extends the standard GTK+ 3.x
Summary(pl.UTF-8):	Widget tekstowy rozszerzający standardowy z GTK+ 3.x
Name:		gtksourceview5
Version:	5.12.0
Release:	1
License:	LGPL v2+ (library), GPL v2+ (some language specs files)
Group:		X11/Libraries
Source0:	https://download.gnome.org/sources/gtksourceview/5.12/gtksourceview-%{version}.tar.xz
# Source0-md5:	60ed6cd89cc877c2e7e08d314fa55e02
Patch0:		%{name}-no-update.patch
URL:		https://wiki.gnome.org/Projects/GtkSourceView
BuildRequires:	docbook-dtd412-xml
BuildRequires:	fontconfig-devel
BuildRequires:	fribidi-devel >= 0.19.7
BuildRequires:	gettext-tools >= 0.19.4
%{?with_apidocs:BuildRequires:	gi-docgen}
BuildRequires:	glib2-devel >= 1:2.72
BuildRequires:	gobject-introspection-devel >= 1.70.0
BuildRequires:	gtk4-devel >= 4.6
BuildRequires:	itstool
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	meson >= 0.60.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pango-devel
BuildRequires:	pcre2-8-devel >= 10.21
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.029
BuildRequires:	sed >= 4.0
%{?with_sysprof:BuildRequires:	sysprof-devel >= 3.38}
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
BuildRequires:	xz
Requires:	fribidi >= 0.19.7
Requires:	glib2 >= 1:2.72
Requires:	gtk4 >= 4.6
Requires:	libxml2 >= 1:2.6.31
Requires:	pcre2-8 >= 10.21
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GtkSourceView is a text widget that extends the standard GTK+ 3.x text
widget GtkTextView. It improves GtkTextView by implementing syntax
highlighting and other features typical of a source editor.

%description -l pl.UTF-8
GtkSourceView to widget tekstowy rozszerzający standardowy widget
tekstowy GtkTextView z GTK+ 3.x. Ulepsza GtkTextView poprzez
zaimplementowanie podświetlania składni i innych możliwości typowych
dla edytora źródeł.

%package devel
Summary:	Header files for GtkSourceView
Summary(pl.UTF-8):	Pliki nagłówkowe dla GtkSourceView
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	fribidi-devel >= 0.19.7
Requires:	glib2-devel >= 1:2.72
Requires:	gtk4-devel >= 4.6
Requires:	libxml2-devel >= 1:2.6.31
Requires:	pcre2-8-devel >= 10.21

%description devel
Header files for GtkSourceView.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla GtkSourceView.

%package static
Summary:	Static GtkSourceView library
Summary(pl.UTF-8):	Statyczna biblioteka GtkSourceView
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GtkSourceView library.

%description static -l pl.UTF-8
Statyczna biblioteka GtkSourceView.

%package apidocs
Summary:	GtkSourceView API documentation
Summary(pl.UTF-8):	Dokumentacja API GtkSourceView
Group:		Documentation
BuildArch:	noarch

%description apidocs
GtkSourceView API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API GtkSourceView.

%package -n vala-gtksourceview5
Summary:	GtkSourceView API for Vala language
Summary(pl.UTF-8):	API GtkSourceView dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
BuildArch:	noarch

%description -n vala-gtksourceview5
GtkSourceView API for Vala language.

%description -n vala-gtksourceview5 -l pl.UTF-8
API GtkSourceView dla języka Vala.

%prep
%setup -q -n gtksourceview-%{version}
%patch0 -p1

%if %{with static_libs}
%{__sed} -i -e 's/gtksource_lib = shared_library/gtksource_lib = library/' gtksourceview/meson.build
%endif

%build
%meson build \
	%{?with_apidocs:-Ddocumentation=true} \
	%{?with_sysprof:-Dsysprof=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/gtksourceview5 $RPM_BUILD_ROOT%{_gidocdir}
%endif

# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang gtksourceview-5

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f gtksourceview-5.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgtksourceview-5.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgtksourceview-5.so.0
%{_datadir}/gtksourceview-5
%{_libdir}/girepository-1.0/GtkSource-5.typelib
%{_iconsdir}/hicolor/scalable/actions/completion-*-symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/lang-*-symbolic.svg

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgtksourceview-5.so
%{_includedir}/gtksourceview-5
%{_pkgconfigdir}/gtksourceview-5.pc
%{_datadir}/gir-1.0/GtkSource-5.gir

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgtksourceview-5.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/gtksourceview5
%endif

%if %{with vala}
%files -n vala-gtksourceview5
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gtksourceview-5.deps
%{_datadir}/vala/vapi/gtksourceview-5.vapi
%endif
