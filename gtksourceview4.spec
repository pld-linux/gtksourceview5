#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_with 	glade		# install glade catalog
%bcond_without	static_libs	# static library
%bcond_without	vala		# do not build Vala API

Summary:	Text widget that extends the standard GTK+ 3.x
Summary(pl.UTF-8):	Widget tekstowy rozszerzający standardowy z GTK+ 3.x
Name:		gtksourceview4
Version:	4.8.1
Release:	1
License:	LGPL v2+ (library), GPL v2+ (some language specs files)
Group:		X11/Libraries
Source0:	https://download.gnome.org/sources/gtksourceview/4.8/gtksourceview-%{version}.tar.xz
# Source0-md5:	d10c624feb48412542f9e3447e75d6bc
URL:		https://wiki.gnome.org/Projects/GtkSourceView
BuildRequires:	docbook-dtd412-xml
BuildRequires:	fribidi-devel >= 0.19.7
BuildRequires:	gettext-tools >= 0.19.4
BuildRequires:	glib2-devel >= 1:2.48.0
BuildRequires:	gobject-introspection-devel >= 1.42.0
BuildRequires:	gtk+3-devel >= 3.24
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.25}
BuildRequires:	itstool
%if %{with glade}
BuildRequires:	libgladeui-devel >= 3.9.0
%endif
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	meson >= 0.50.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
BuildRequires:	xz
Requires:	fribidi >= 0.19.7
Requires:	glib2 >= 1:2.48.0
Requires:	gtk+3 >= 3.24
Requires:	libxml2 >= 1:2.6.31
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
Requires:	glib2-devel >= 1:2.48.0
Requires:	gtk+3-devel >= 3.24
Requires:	libxml2-devel >= 1:2.6.31

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
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
GtkSourceView API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API GtkSourceView.

%package -n glade3-gtksourceview
Summary:	Glade3 catalog entry for GtkSourceView library
Summary(pl.UTF-8):	Wpis katalogu Glade3 dla biblioteki GtkSourceView
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	libgladeui >= 3.9.0

%description -n glade3-gtksourceview
Glade3 catalog entry for GtkSourceView library.

%description -n glade3-gtksourceview -l pl.UTF-8
Wpis katalogu Glade3 dla biblioteki GtkSourceView.

%package -n vala-gtksourceview4
Summary:	GtkSourceView API for Vala language
Summary(pl.UTF-8):	API GtkSourceView dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
BuildArch:	noarch

%description -n vala-gtksourceview4
GtkSourceView API for Vala language.

%description -n vala-gtksourceview4 -l pl.UTF-8
API GtkSourceView dla języka Vala.

%prep
%setup -q -n gtksourceview-%{version}

%if %{with static_libs}
%{__sed} -i -e 's/gtksource_lib = shared_library/gtksource_lib = library/' gtksourceview/meson.build
%endif

%build
%meson build \
	%{?with_glade:-Dglade_catalog=true} \
	%{?with_apidocs:-Dgtk_doc=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang gtksourceview-4

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f gtksourceview-4.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgtksourceview-4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgtksourceview-4.so.0
%{_datadir}/gtksourceview-4
%{_libdir}/girepository-1.0/GtkSource-4.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgtksourceview-4.so
%{_includedir}/gtksourceview-4
%{_pkgconfigdir}/gtksourceview-4.pc
%{_datadir}/gir-1.0/GtkSource-4.gir

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgtksourceview-4.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gtksourceview-4.0
%endif

%if %{with glade}
%files -n glade3-gtksourceview
%defattr(644,root,root,755)
%{_datadir}/glade3/catalogs/gtksourceview.xml
%endif

%if %{with vala}
%files -n vala-gtksourceview4
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gtksourceview-4.deps
%{_datadir}/vala/vapi/gtksourceview-4.vapi
%endif
